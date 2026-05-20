from fastapi import APIRouter

from app.schemas.payment import ChatRequest, ChatResponse
from app.services import payment_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse, summary="Convert merchant chat into payment intent")
async def chat(req: ChatRequest) -> ChatResponse:
    """Send a natural-language merchant request, get back a structured payment + link + WhatsApp message."""
    return await payment_service.handle_chat(req.message, req.merchant_id)
