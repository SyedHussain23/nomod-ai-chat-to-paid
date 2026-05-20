from collections import Counter
from typing import Any

from app.database.db import db


def dashboard_metrics(merchant_id: str = "mch_demo") -> dict[str, Any]:
    rows = [r for r in db.table("payments") if r.get("merchant_id") == merchant_id]
    status_counts = Counter(r.get("status", "pending") for r in rows)
    total_volume = sum(float(r.get("amount", 0)) for r in rows)
    paid_volume = sum(float(r.get("amount", 0)) for r in rows if r.get("status") == "paid")
    pending_volume = sum(float(r.get("amount", 0)) for r in rows if r.get("status") == "pending")
    escalations = sum(1 for r in rows if r.get("escalation_required"))
    urgency_counts = Counter(r.get("urgency", "medium") for r in rows)
    categories = Counter(r.get("payment_category", "other") for r in rows)

    return {
        "totals": {
            "requests": len(rows),
            "pending": status_counts.get("pending", 0),
            "paid": status_counts.get("paid", 0),
            "overdue": status_counts.get("overdue", 0),
            "failed": status_counts.get("failed", 0),
            "escalations": escalations,
        },
        "volume": {
            "currency": "AED",
            "total": round(total_volume, 2),
            "paid": round(paid_volume, 2),
            "pending": round(pending_volume, 2),
            "collection_rate": round((paid_volume / total_volume * 100) if total_volume else 0, 1),
        },
        "urgency_breakdown": dict(urgency_counts),
        "category_breakdown": dict(categories),
    }
