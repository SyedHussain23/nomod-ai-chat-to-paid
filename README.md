# Nomod AI — Chat to Paid in Seconds

> AI-native merchant operations assistant for [Nomod](https://nomod.com/en-ae) — turn a sentence like
> *"Charge Ahmed 500 AED for AC repair"* into a payment link, a WhatsApp message, status tracking,
> and an automated follow-up loop.

This is a production-style MVP built as a Product Engineer interview project. It is intentionally
focused on rapid MVP execution with scalable modular architecture and AI-native workflow design
rather than overengineering.

---

## 1. Problem Statement

UAE SMB merchants — AC repair shops, salons, freelancers, home-services operators — lose hours every
week to payment operations:

- Manually crafting WhatsApp invoices for each customer.
- Forgetting to follow up on unpaid links.
- Spotting frustrated customers too late, after refunds escalate.
- Reconciling dozens of payment links from a mobile screen.

The merchant doesn't need another dashboard. They need an **operations agent** that understands
intent, builds the artifacts, and chases the money.

## 2. Solution Overview

Nomod AI is a merchant-facing assistant. The merchant types in plain English (or Arabic-mixed
English) — Claude extracts a structured payment intent, the backend mints a Nomod-style payment
link, generates a professional WhatsApp message, and starts an automated lifecycle:

1. **Extraction** — Claude turns text into typed JSON (customer, amount, currency, urgency,
   sentiment, escalation flag).
2. **Link generation** — backend mints a Nomod-style short link (`pay.nomod.ai/pay/<token>`).
3. **WhatsApp draft** — Claude writes a tone-appropriate message.
4. **Lifecycle** — webhook simulator updates status; AI generates progressively firmer follow-ups.
5. **Observability** — every event lands in a merchant activity feed and KPIs roll up to a dashboard.

## 3. Architecture

```
┌─────────────────────────┐         ┌────────────────────────────────────────┐
│   React + TS + Tailwind │  HTTP   │           FastAPI (async)              │
│  Assistant · Payments   │ ◀────▶  │  /api/ai  /api/payments  /api/dashboard │
│  · Analytics dashboard  │         │                                        │
└─────────────────────────┘         │   services/ ─ payment, analytics,      │
                                    │              activity                  │
                                    │   ai/       ─ claude_client,           │
                                    │              extractor, followup       │
                                    │   schemas/  ─ Pydantic v2 models       │
                                    │   middleware/ logging + request-id     │
                                    │   database/ ─ MockDB (PG-ready shape)  │
                                    └──────────────────┬─────────────────────┘
                                                       │
                                              ┌────────▼────────┐
                                              │  Claude API     │
                                              │  (JSON-mode +   │
                                              │   text drafts)  │
                                              └─────────────────┘
```

- **Backend** — FastAPI, async end-to-end, Pydantic v2 schemas, request-id logging middleware,
  modular service layer cleanly separated from AI orchestration. The mock store is shaped exactly
  like a Postgres schema (`payments`, `activity`, `followups`, `merchants`) so it ports to SQLModel
  / SQLAlchemy in one swap.
- **AI Layer** — One thin Anthropic client (`claude_client.py`) with retry, JSON-mode parsing, and
  graceful fallback. Two orchestrators on top — `extractor.py` (intent extraction) and
  `followup.py` (WhatsApp + reminders). Each has a heuristic fallback so the demo works even
  without an API key.
- **Frontend** — Vite + React 18 + TypeScript + Tailwind. Three views: **Assistant** (chat + live
  feed), **Payments** (filterable card grid), **Analytics** (KPIs, urgency mix, activity).
- **Webhook simulation** — `POST /api/payments/{id}/webhook/paid` mimics the provider callback that
  will land in production.

## 4. Features

**Core (implemented)**
- AI extraction of customer, amount, currency, service, urgency, sentiment, escalation.
- Nomod-style payment link minting.
- AI-drafted WhatsApp message per payment.
- Merchant dashboard — totals, collection rate, escalation count, urgency & category mix.
- Priority detection (low / medium / high).
- Sentiment + escalation detection (frustrated / refund risk).
- Activity log of every operational event.
- Payment status lifecycle (pending → paid / overdue / failed).
- AI follow-up generation that escalates tone with each reminder (gentle → firm → urgent).

**Bonus (implemented)**
- Webhook simulator endpoint.
- Retry-safe AI client with exponential backoff.
- Graceful heuristic fallback when `ANTHROPIC_API_KEY` is unset — demo never breaks.
- Request-id logging middleware.
- Docker + docker-compose for one-command boot.
- Mock DB shaped for Postgres migration.

## 5. AI Workflow Design

**Extraction prompt** (`backend/app/ai/extractor.py`) returns strict JSON. We use a JSON-block
regex extractor on the response, validate with Pydantic, and on any parse/validation failure fall
back to a deterministic regex heuristic so the merchant never sees a broken request.

**Tone-aware follow-up** (`backend/app/ai/followup.py`) reads `followup_count` and asks Claude to
shift tone:

| Followup # | Tone   |
|------------|--------|
| 1          | gentle |
| 2          | firm   |
| 3+         | urgent (mentions escalation) |

**Retry & safety** — `ClaudeClient.json_call` retries with backoff, logs failures, and returns
`None` on exhaustion so the calling service can fall back rather than 500.

## 6. Scalability Roadmap

- **Real payment APIs** — replace `BASE_PAYMENT_URL` mint with Nomod's link API; webhook handler
  already wired.
- **Async queues** — move follow-up scheduling onto Celery / Arq with Redis; today's stub keeps
  the shape.
- **Observability** — wire OpenTelemetry on the FastAPI app; the request-id middleware is the
  hook point.
- **Multi-agent workflows** — split `extractor`, `dunning-agent`, `escalation-agent`, and
  `recon-agent` into supervised tools behind a router.
- **RAG-ready** — merchant history + customer history become retrieval sources for personalized
  follow-up drafts.
- **Fraud detection** — score every extraction (amount anomaly, velocity, sentiment) before mint.
- **Multilingual** — Claude already handles Arabic; add `locale` to the schema and template
  WhatsApp messages.
- **Auth** — JWT-ready structure; `merchant_id` is already threaded end-to-end.

## 7. Local Setup

### Option A — Docker (recommended)

```bash
cp .env.example .env       # add ANTHROPIC_API_KEY (optional — fallback works without)
docker compose up --build
# Frontend → http://localhost:3000
# Backend  → http://localhost:8000/docs
```

### Option B — Native dev

```bash
# Backend
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # add ANTHROPIC_API_KEY
uvicorn app.main:app --reload --port 8000

# Frontend (separate shell)
cd frontend
npm install
npm run dev                # http://localhost:5173
```

Or one-shot: `./scripts/start.sh`.

## 8. API Documentation

Full OpenAPI: **http://localhost:8000/docs**

| Method | Path | Purpose |
|--------|------|---------|
| POST   | `/api/ai/chat` | NL request → extraction + payment + WhatsApp msg |
| GET    | `/api/payments` | List all payments for a merchant |
| GET    | `/api/payments/{id}` | Single payment |
| PATCH  | `/api/payments/{id}/status` | Update status (`pending`/`paid`/`overdue`/`failed`) |
| POST   | `/api/payments/{id}/followup` | Generate AI follow-up reminder |
| POST   | `/api/payments/{id}/webhook/paid` | Simulated provider webhook |
| GET    | `/api/dashboard/metrics` | KPIs, volume, breakdowns |
| GET    | `/api/dashboard/activity` | Recent activity feed |

### Sample requests

```bash
# Create a payment from natural language
curl -X POST http://localhost:8000/api/ai/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Charge Ahmed 500 AED for AC repair, urgent"}'

# Simulate payment received
curl -X POST http://localhost:8000/api/payments/pay_abc123/webhook/paid

# Trigger AI follow-up
curl -X POST http://localhost:8000/api/payments/pay_abc123/followup
```

### Sample merchant interactions

| Merchant types | AI extracts |
|---|---|
| "Charge Ahmed 500 AED for AC repair" | customer=Ahmed, amount=500, urgency=medium, category=repair |
| "Bill Fatima 1250 for monthly cleaning, urgent" | urgency=high, category=service |
| "Invoice Khalid 3200 — he's been asking for a refund" | sentiment=frustrated, escalation_required=true |
| "Send Layla 75 AED link for delivery" | category=service, amount=75 |

## 9. Screenshots

> Spin up locally (`docker compose up`) and the Vite/React app at `http://localhost:3000` shows:
> Assistant (chat + activity), Payments (filterable cards), Analytics (KPIs + breakdowns).

## 10. Deployment

- **Frontend → Vercel** — root `frontend/`, build `npm run build`, output `dist`, env
  `VITE_API_BASE=https://<api>.onrender.com/api`.
- **Backend → Render / Railway** — root `backend/`, start
  `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, env `ANTHROPIC_API_KEY`, mount a small
  persistent disk on `/app/data` if you want the JSON store to survive deploys (or swap to
  Postgres before shipping).

## Product Engineering Philosophy

I intentionally focused on **rapid MVP execution with scalable modular architecture and AI-native
workflow design rather than overengineering.** Every piece is the smallest credible version of
the production thing:

- The mock DB is shaped like Postgres so the migration is mechanical.
- The Claude client is one file with retry, JSON parsing, and a fallback — small enough to read in
  60 seconds, structured enough to extend.
- Services are pure functions over the store, so they're trivial to test or swap to real Nomod APIs.
- The UI prioritises operational density (cards, badges, activity feed) over decorative chrome —
  it feels like fintech ops software, not a chatbot demo.

The goal: something an AI-native startup engineer would prototype in a high-velocity fintech team
on day one, ship to a real merchant on day three, and harden into production by week two.
