import logging
import time
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("nomod-ai")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = uuid4().hex[:8]
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception as exc:
            logger.exception("req=%s %s %s failed: %s", request_id, request.method, request.url.path, exc)
            raise
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "req=%s %s %s -> %s in %.1fms",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        response.headers["x-request-id"] = request_id
        return response
