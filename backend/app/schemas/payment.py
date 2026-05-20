from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

Urgency = Literal["low", "medium", "high"]
PaymentStatus = Literal["pending", "paid", "overdue", "failed"]
Sentiment = Literal["neutral", "satisfied", "frustrated", "at_risk"]


class ExtractedRequest(BaseModel):
    customer_name: str
    amount: float
    currency: str = "AED"
    service_description: str
    payment_category: str
    urgency: Urgency = "medium"
    sentiment: Sentiment = "neutral"
    escalation_required: bool = False
    notes: Optional[str] = None


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    merchant_id: str = "mch_demo"


class PaymentRecord(BaseModel):
    id: str
    merchant_id: str
    customer_name: str
    amount: float
    currency: str
    service_description: str
    payment_category: str
    urgency: Urgency
    sentiment: Sentiment
    escalation_required: bool
    status: PaymentStatus = "pending"
    payment_link: str
    whatsapp_message: str
    created_at: datetime
    paid_at: Optional[datetime] = None
    followup_count: int = 0


class ChatResponse(BaseModel):
    payment: PaymentRecord
    extraction: ExtractedRequest
    ai_summary: str


class FollowupResponse(BaseModel):
    payment_id: str
    message: str
    tone: str
    channel: Literal["whatsapp", "sms", "email"] = "whatsapp"


class StatusUpdate(BaseModel):
    status: PaymentStatus
