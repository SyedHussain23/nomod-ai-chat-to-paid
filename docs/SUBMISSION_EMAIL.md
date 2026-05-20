# Nomod Submission Email

**Subject:** Product Engineer (AI-Native) — Nomod AI: Chat to Paid in Seconds

---

Hi Team,

For the Product Engineer (AI-Native) role, I built **Nomod AI — Chat to Paid in Seconds**: a merchant operations assistant that turns one English sentence ("Charge Ahmed 500 AED for AC repair") into a Nomod-style payment link, a WhatsApp draft, lifecycle tracking, and an automated follow-up loop.

**Why this product, for Nomod**
UAE SMB merchants already run on WhatsApp and payment links — Nomod's primitives. The next unlock is an AI-native layer that operates *on top of* those primitives: the merchant types, the agent executes. This MVP is that layer.

**What's in the box**
- **AI extraction** — Claude turns NL into a typed payment intent (customer, amount, urgency, sentiment, escalation). Strict JSON, Pydantic-validated, deterministic fallback so the demo never breaks.
- **Payment + WhatsApp generation** — link minted, tone-aware draft written in the same call chain.
- **Lifecycle + webhooks** — pending → paid / overdue / failed, with a webhook-simulator endpoint that mirrors the real provider callback.
- **Tone-escalating follow-ups** — gentle → firm → urgent based on reminder count.
- **Ops dashboard** — collection rate, escalations, urgency & category mix, live activity feed.
- **Production-shaped architecture** — FastAPI (async), Pydantic v2, modular services, request-id logging, Postgres-shaped mock DB, Docker + docker-compose, Vercel + Render configs.

**Links**
- Live frontend: `https://nomod-ai.vercel.app`
- Live API + docs: `https://nomod-ai-backend.onrender.com/docs`
- Repo: `https://github.com/<you>/nomod-ai-chat-to-paid`
- 75-second Loom: `https://www.loom.com/share/<id>`

**Engineering philosophy**
I intentionally focused on **rapid MVP execution with scalable modular architecture and AI-native workflow design rather than overengineering.** Every layer is the smallest credible version of the production thing: the mock DB has the production schema, the AI client is one file with retry + fallback, services are pure functions over the store. The system is built to be swapped, not rewritten.

Happy to discuss whenever works for you.

Best,
Syed Hussain Abdul Hakeem

---
