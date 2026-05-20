"""AI extraction: natural-language merchant request -> structured payment intent."""
from __future__ import annotations

import re

from app.ai.claude_client import claude
from app.schemas.payment import ExtractedRequest

SYSTEM_PROMPT = """You are an AI operations agent for Nomod, a UAE payment infrastructure company.
You convert free-text merchant requests into a structured JSON payment intent.

Return ONLY a JSON object with these exact keys:
{
  "customer_name": str,
  "amount": number,
  "currency": "AED" | "USD" | "SAR" | "EUR" | "GBP",
  "service_description": str (3-8 words, professional),
  "payment_category": one of ["repair", "service", "product", "consultation", "subscription", "rental", "other"],
  "urgency": "low" | "medium" | "high",
  "sentiment": "neutral" | "satisfied" | "frustrated" | "at_risk",
  "escalation_required": boolean,
  "notes": string or null
}

Rules:
- Default currency is AED for UAE merchants.
- Detect urgency from words like "urgent", "asap", "today", "overdue".
- Detect frustration / escalation from words like "angry", "refund", "complaint", "third reminder".
- Never invent amounts. If amount is missing, set amount=0 and escalation_required=true.
- Be concise. Output JSON only — no prose, no markdown fences."""


_FALLBACK_AMOUNT_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(aed|usd|sar|eur|gbp)?", re.IGNORECASE)
_CHARGE_NAME_RE = re.compile(r"charge\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)", re.IGNORECASE)


def _heuristic_fallback(message: str) -> ExtractedRequest:
    """Used when Claude API is not configured or fails — keeps the demo usable."""
    amount = 0.0
    currency = "AED"
    m = _FALLBACK_AMOUNT_RE.search(message)
    if m:
        try:
            amount = float(m.group(1).replace(",", ""))
        except ValueError:
            amount = 0.0
        if m.group(2):
            currency = m.group(2).upper()

    name_match = _CHARGE_NAME_RE.search(message)
    customer = name_match.group(1).title() if name_match else "Customer"

    lower = message.lower()
    urgency = "high" if any(w in lower for w in ("urgent", "asap", "today", "overdue")) else "medium"
    sentiment = "frustrated" if any(w in lower for w in ("angry", "complaint", "refund", "frustrated")) else "neutral"
    escalation = sentiment == "frustrated" or "refund" in lower

    # crude service description: text after "for"
    desc = "General service"
    if " for " in lower:
        desc = message.split(" for ", 1)[1].strip().rstrip(".").title()[:60] or desc

    return ExtractedRequest(
        customer_name=customer,
        amount=amount,
        currency=currency,
        service_description=desc,
        payment_category="service",
        urgency=urgency,  # type: ignore[arg-type]
        sentiment=sentiment,  # type: ignore[arg-type]
        escalation_required=escalation,
        notes="Parsed via heuristic fallback — set ANTHROPIC_API_KEY for AI extraction.",
    )


async def extract_payment_intent(message: str) -> ExtractedRequest:
    if claude.enabled:
        data = await claude.json_call(system=SYSTEM_PROMPT, user=message, max_tokens=500)
        if data:
            try:
                return ExtractedRequest(**data)
            except Exception:
                pass
    return _heuristic_fallback(message)
