from fastapi import APIRouter, HTTPException

from app.schemas.payment import FollowupResponse, PaymentRecord, StatusUpdate
from app.services import payment_service

router = APIRouter()


@router.get("", response_model=list[PaymentRecord], summary="List merchant payments")
async def list_all(merchant_id: str = "mch_demo") -> list[PaymentRecord]:
    return [PaymentRecord(**r) for r in payment_service.list_payments(merchant_id)]


@router.get("/{payment_id}", response_model=PaymentRecord)
async def get_one(payment_id: str) -> PaymentRecord:
    row = payment_service.get_payment(payment_id)
    if not row:
        raise HTTPException(404, "payment not found")
    return PaymentRecord(**row)


@router.patch("/{payment_id}/status", response_model=PaymentRecord, summary="Update payment status (webhook sim)")
async def patch_status(payment_id: str, body: StatusUpdate) -> PaymentRecord:
    row = payment_service.update_status(payment_id, body.status)
    if not row:
        raise HTTPException(404, "payment not found")
    return PaymentRecord(**row)


@router.post("/{payment_id}/followup", response_model=FollowupResponse, summary="Generate AI follow-up")
async def followup(payment_id: str) -> FollowupResponse:
    resp = await payment_service.followup_for(payment_id)
    if not resp:
        raise HTTPException(404, "payment not found")
    return resp


@router.post("/{payment_id}/webhook/paid", response_model=PaymentRecord, summary="Simulated payment-provider webhook")
async def webhook_paid(payment_id: str) -> PaymentRecord:
    row = payment_service.update_status(payment_id, "paid")
    if not row:
        raise HTTPException(404, "payment not found")
    return PaymentRecord(**row)
