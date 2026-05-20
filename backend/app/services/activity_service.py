from datetime import datetime, timezone
from typing import Any

from app.database.db import db
from app.utils.ids import short_id


def log(event: str, *, merchant_id: str = "mch_demo", payload: dict[str, Any] | None = None) -> dict[str, Any]:
    entry = {
        "id": f"act_{short_id(8)}",
        "merchant_id": merchant_id,
        "event": event,
        "payload": payload or {},
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    db.insert("activity", entry)
    return entry


def recent(limit: int = 30, merchant_id: str = "mch_demo") -> list[dict[str, Any]]:
    rows = [r for r in db.table("activity") if r.get("merchant_id") == merchant_id]
    return sorted(rows, key=lambda r: r["created_at"], reverse=True)[:limit]
