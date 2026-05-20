"""AI-generated follow-up reminders and WhatsApp messages."""
from __future__ import annotations

from app.ai.claude_client import claude
from app.schemas.payment import ExtractedRequest, PaymentRecord


WHATSAPP_SYSTEM = """You write short, professional WhatsApp payment-request messages for UAE merchants on Nomod.
Tone: friendly, concise, business-appropriate. 2-4 short lines. Always include the payment link.
Never use emoji clutter — at most one subtle emoji. Output the message only, no quotes, no markdown."""

FOLLOWUP_SYSTEM = """You write professional follow-up payment reminders for UAE merchants on Nomod.
Adjust tone by `followup_count`:
- 1: gentle nudge
- 2: firm but polite
- 3+: urgent, mention escalation respectfully

2-4 short lines, include the payment link, no emoji clutter. Output the message only."""


def _fallback_whatsapp(extraction: ExtractedRequest, link: str) -> str:
    return (
        f"Hi {extraction.customer_name}, this is {extraction.service_description}.\n"
        f"Amount due: {extraction.currency} {extraction.amount:.2f}.\n"
        f"Pay securely via Nomod: {link}\n"
        f"Thank you."
    )


def _fallback_followup(payment: PaymentRecord) -> str:
    n = payment.followup_count + 1
    if n == 1:
        opener = f"Hi {payment.customer_name}, friendly reminder for your pending payment"
    elif n == 2:
        opener = f"Hi {payment.customer_name}, your payment is still pending"
    else:
        opener = f"Hi {payment.customer_name}, this is our final reminder before escalation"
    return (
        f"{opener}.\n"
        f"{payment.service_description} — {payment.currency} {payment.amount:.2f}.\n"
        f"Pay now: {payment.payment_link}"
    )


async def generate_whatsapp_message(extraction: ExtractedRequest, link: str) -> str:
    if claude.enabled:
        user = (
            f"Customer: {extraction.customer_name}\n"
            f"Service: {extraction.service_description}\n"
            f"Amount: {extraction.currency} {extraction.amount:.2f}\n"
            f"Urgency: {extraction.urgency}\n"
            f"Payment link: {link}"
        )
        text = await claude.text_call(system=WHATSAPP_SYSTEM, user=user, max_tokens=200)
        if text:
            return text
    return _fallback_whatsapp(extraction, link)


async def generate_followup(payment: PaymentRecord) -> str:
    if claude.enabled:
        user = (
            f"Customer: {payment.customer_name}\n"
            f"Service: {payment.service_description}\n"
            f"Amount: {payment.currency} {payment.amount:.2f}\n"
            f"Status: {payment.status}\n"
            f"Followup count so far: {payment.followup_count}\n"
            f"Payment link: {payment.payment_link}"
        )
        text = await claude.text_call(system=FOLLOWUP_SYSTEM, user=user, max_tokens=220)
        if text:
            return text
    return _fallback_followup(payment)
