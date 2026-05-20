"""Thin wrapper around Anthropic SDK with retry and JSON-mode helpers."""
from __future__ import annotations

import asyncio
import json
import logging
import re
from typing import Any

from anthropic import APIError, AsyncAnthropic

from app.config import settings

logger = logging.getLogger("nomod-ai.claude")

_JSON_BLOCK = re.compile(r"\{[\s\S]*\}")


class ClaudeClient:
    def __init__(self) -> None:
        self._client: AsyncAnthropic | None = None
        if settings.anthropic_api_key:
            self._client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    @property
    def enabled(self) -> bool:
        return self._client is not None

    async def json_call(
        self,
        *,
        system: str,
        user: str,
        max_tokens: int = 800,
        retries: int = 2,
    ) -> dict[str, Any] | None:
        """Call Claude and return parsed JSON, or None when unavailable / unparseable."""
        if not self._client:
            return None

        attempt = 0
        last_err: Exception | None = None
        while attempt <= retries:
            try:
                resp = await self._client.messages.create(
                    model=settings.claude_model,
                    max_tokens=max_tokens,
                    system=system,
                    messages=[{"role": "user", "content": user}],
                )
                text = "".join(
                    block.text for block in resp.content if getattr(block, "type", "") == "text"
                )
                match = _JSON_BLOCK.search(text)
                if not match:
                    raise ValueError("no JSON object in response")
                return json.loads(match.group(0))
            except (APIError, ValueError, json.JSONDecodeError) as exc:
                last_err = exc
                logger.warning("claude attempt %d failed: %s", attempt + 1, exc)
                await asyncio.sleep(0.4 * (attempt + 1))
                attempt += 1
        logger.error("claude json_call exhausted retries: %s", last_err)
        return None

    async def text_call(self, *, system: str, user: str, max_tokens: int = 400) -> str | None:
        if not self._client:
            return None
        try:
            resp = await self._client.messages.create(
                model=settings.claude_model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return "".join(
                block.text for block in resp.content if getattr(block, "type", "") == "text"
            ).strip()
        except APIError as exc:
            logger.error("claude text_call failed: %s", exc)
            return None


claude = ClaudeClient()
