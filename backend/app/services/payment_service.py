from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.ai.extractor import extract_payment_intent
from app.ai.followup import generate_followup, generate_whatsapp_message
from app.config import settings
from app.database.db import db
from app.schemas.payment import (
    ChatResponse,
    ExtractedRequest,
    FollowupResponse,
    PaymentRecord,
    PaymentStatus,
)
from app.services import activity_service
from app.utils.ids import link_token, payment_id


def _build_link() -> str:
    return f"{settings.base_payment_url}/{link_token()}"


def _ai_summary(extraction: ExtractedRequest) -> str:
    bits = [
        f"Charging {extraction.customer_name}",
        f"{extraction.currency} {extraction.amount:.2f}",
        f"for {extraction.service_description}",
    ]
    if extraction.urgency == "high":
        bits.append("(marked URGENT)")
    if extraction.escalation_required:
        bits.append("— escalation flagged")
    return " ".join(bits) + "."


async def handle_chat(message: str, merchant_id: str) -> ChatResponse:
    extraction = await extract_payment_intent(message)
    link = _build_link()
    whatsapp = await generate_whatsapp_message(extraction, link)

    record = PaymentRecord(
        id=payment_id(),
        merchant_id=merchant_id,
        customer_name=extraction.customer_name,
        amount=extraction.amount,
        currency=extraction.currency,
        service_description=extraction.service_description,
        payment_category=extraction.payment_category,
        urgency=extraction.urgency,
        sentiment=extraction.sentiment,
        escalation_required=extraction.escalation_required,
        status="pending",
        payment_link=link,
        whatsapp_message=whatsapp,
        created_at=datetime.now(timezone.utc),
    )
    db.insert("payments", record.model_dump(mode="json"))
    activity_service.log(
        "payment.created",
        merchant_id=merchant_id,
        payload={"payment_id": record.id, "amount": record.amount, "customer": record.customer_name},
    )
    if extraction.escalation_required:
        activity_service.log(
            "escalation.flagged",
            merchant_id=merchant_id,
            payload={"payment_id": record.id, "reason": extraction.sentiment},
        )

    return ChatResponse(payment=record, extraction=extraction, ai_summary=_ai_summary(extraction))


def list_payments(merchant_id: str = "mch_demo") -> list[dict[str, Any]]:
    rows = [r for r in db.table("payments") if r.get("merchant_id") == merchant_id]
    return sorted(rows, key=lambda r: r["created_at"], reverse=True)


def get_payment(payment_id_: str) -> dict[str, Any] | None:
    return db.find("payments", payment_id_)


def update_status(payment_id_: str, status: PaymentStatus) -> dict[str, Any] | None:
    patch: dict[str, Any] = {"status": status}
    if status == "paid":
        patch["paid_at"] = datetime.now(timezone.utc).isoformat()
    updated = db.update("payments", payment_id_, patch)
    if updated:
        activity_service.log(
            f"payment.{status}",
            merchant_id=updated.get("merchant_id", "mch_demo"),
            payload={"payment_id": payment_id_},
        )
    return updated


async def followup_for(payment_id_: str) -> FollowupResponse | None:
    raw = db.find("payments", payment_id_)
    if not raw:
        return None
    record = PaymentRecord(**raw)
    message = await generate_followup(record)
    new_count = record.followup_count + 1
    db.update("payments", payment_id_, {"followup_count": new_count})
    tone = "gentle" if new_count == 1 else "firm" if new_count == 2 else "urgent"
    activity_service.log(
        "followup.sent",
        merchant_id=record.merchant_id,
        payload={"payment_id": payment_id_, "tone": tone, "count": new_count},
    )
    db.insert(
        "followups",
        {
            "payment_id": payment_id_,
            "message": message,
            "tone": tone,
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
    )
    return FollowupResponse(payment_id=payment_id_, message=message, tone=tone)
