<div align="center">

# Nomod AI — Chat to Paid in Seconds

**An AI-native merchant operations assistant for [Nomod](https://nomod.com/en-ae).**
Type *"Charge Ahmed 500 AED for AC repair"* — get a payment link, a WhatsApp draft, lifecycle tracking, and automated follow-ups in one shot.

[![FastAPI](https://img.shields.io/badge/FastAPI-async-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind](https://img.shields.io/badge/Tailwind-3-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Claude](https://img.shields.io/badge/Claude-Anthropic-D97757?logo=anthropic&logoColor=white)](https://www.anthropic.com/)
[![Docker](https://img.shields.io/badge/Docker-compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-black)](LICENSE)

> **AI-native, fintech-aware, operations-first.** Built end-to-end as a production-style MVP for the Nomod Product Engineer interview.

</div>

---

## 1. The Problem

UAE SMB merchants — AC technicians, salons, freelancers, home-services operators — run their business in WhatsApp. They also lose hours every week to **payment operations**:

- **Manual invoice drafting** — every quote, every link, every reminder is hand-typed on a phone.
- **Forgotten follow-ups** — unpaid links sit untouched while cash flow tightens.
- **Sentiment blind spots** — a frustrated customer is only spotted after the refund request.
- **Reconciliation chaos** — dozens of links across WhatsApp chats with no central view.

These merchants don't need another dashboard. They need an **operations agent** that understands intent, builds the artifacts, chases the money, and tells them when something needs human attention.

## 2. Why This Matters For Nomod

Nomod already wins on the four primitives that matter to UAE SMBs: **payment links, merchant ops, conversational commerce, and mobile-first checkout**. The next unlock is AI-native workflow orchestration on top of those primitives.

| Nomod's product | What this MVP adds |
|---|---|
| Payment links | Created from a single English sentence, no form-filling. |
| Merchant ops | Auto-generated WhatsApp drafts, AI follow-ups, escalation flags. |
| Conversational commerce | Natural-language → structured payment intent in one Claude call. |
| Mobile-first SMB | One textbox replaces five fields. The agent does the rest. |

The thesis: **the merchant types, the system operates.** Every operational artifact (link, message, status, follow-up, escalation) is generated and tracked by the agent.

## 3. Solution Overview

A merchant types a charge request in plain English. The system:

1. **Extracts** structured intent — customer, amount, currency, service, urgency, sentiment, escalation flag.
2. **Mints** a Nomod-style payment link.
3. **Drafts** a tone-appropriate WhatsApp message.
4. **Tracks** status (pending → paid / overdue / failed) with a webhook-simulator endpoint.
5. **Escalates tone** automatically across follow-ups (gentle → firm → urgent).
6. **Surfaces** every event in an operations dashboard with KPIs and a live activity feed.

## 4. Product Workflow

```
Merchant types
   "Charge Ahmed 500 AED for AC repair"
            │
            ▼
   ┌──────────────────┐
   │  Claude extract  │   ── structured JSON intent
   └────────┬─────────┘
            ▼
   ┌──────────────────┐
   │  Payment mint    │   ── pay.nomod.ai/pay/<token>
   └────────┬─────────┘
            ▼
   ┌──────────────────┐
   │  WhatsApp draft  │   ── tone-aware, brand-safe
   └────────┬─────────┘
            ▼
   ┌──────────────────┐
   │ Lifecycle + KPIs │   ── status, follow-ups, escalations
   └──────────────────┘
```

See [`docs/architecture/workflow-diagram.md`](docs/architecture/workflow-diagram.md) for the full Mermaid sequence.

## 5. AI Workflow Architecture

The AI layer is intentionally small and orchestratable:

- **`claude_client.py`** — one thin Anthropic wrapper with retry, JSON-block extraction, structured parsing, and graceful fallback. Returns `None` on exhaustion so callers can degrade safely instead of 500-ing.
- **`extractor.py`** — natural-language → typed Pydantic `ExtractedRequest`. Strict JSON system prompt, Pydantic validation, regex fallback so the demo never breaks even without an API key.
- **`followup.py`** — tone-aware reminders that escalate with `followup_count`:

  | Reminder # | Tone |
  |---|---|
  | 1 | gentle nudge |
  | 2 | firm but polite |
  | 3+ | urgent, references escalation |

- **Escalation + urgency** are first-class fields on every payment, surfaced in the UI as badges and on the dashboard as a KPI.
- **Logging** — every AI call and every domain event flows through the activity feed, giving us a built-in audit trail.

See [`docs/architecture/architecture-diagram.md`](docs/architecture/architecture-diagram.md).

## 6. Technical Architecture

```
┌─────────────────────────┐         ┌────────────────────────────────────────┐
│   React 18 + TS + TW    │  HTTP   │           FastAPI (async)              │
│  Assistant · Payments   │ ◀────▶  │  /api/ai  /api/payments  /api/dashboard│
│  · Analytics dashboard  │         │                                        │
└─────────────────────────┘         │  services/  payment · analytics ·      │
                                    │             activity                   │
                                    │  ai/        claude_client · extractor  │
                                    │             · followup                 │
                                    │  schemas/   Pydantic v2                │
                                    │  middleware request-id + structured log│
                                    │  database/  MockDB (Postgres-shaped)   │
                                    └──────────────────┬─────────────────────┘
                                                       │
                                              ┌────────▼────────┐
                                              │  Anthropic API  │
                                              │  Claude 4.x     │
                                              └─────────────────┘
```

| Layer | Tech | Notes |
|---|---|---|
| Frontend | Vite, React 18, TypeScript, TailwindCSS, React Router | Dark fintech aesthetic, dense ops UI |
| Backend | FastAPI, Pydantic v2, async end-to-end | Modular services, request-id logging |
| AI | Anthropic SDK (`claude-opus-4-7`), JSON-mode + retry | Heuristic fallback for demo resilience |
| Storage | JSON-backed `MockDB`, schema-identical to Postgres | One-swap migration to SQLModel |
| Infra | Docker + docker-compose, nginx proxy | Render + Vercel deploy configs included |

## 7. Screenshots

> Drop PNGs into `docs/screenshots/` — names below are referenced in this README.

| | |
|---|---|
| ![Assistant](docs/screenshots/merchant-chat.png) | ![Analytics](docs/screenshots/analytics.png) |
| **Assistant** — chat to paid in seconds | **Analytics** — collection rate, escalations, urgency mix |
| ![Payment flow](docs/screenshots/payment-flow.png) | ![Escalation alerts](docs/screenshots/escalation-alerts.png) |
| **Payment flow** — link + WhatsApp + lifecycle | **Escalations** — frustration + refund risk surfaced early |

Full screenshot list: `dashboard.png`, `merchant-chat.png`, `analytics.png`, `payment-flow.png`, `escalation-alerts.png`.

## 8. Features

**Core**
- ⚡ **One-sentence payments** — Claude turns free text into a typed payment intent.
- 🔗 **Nomod-style links** — minted instantly, ready to send.
- 💬 **WhatsApp drafts** — tone-aware, professional, brand-safe.
- 📊 **Ops dashboard** — totals, collection rate, escalations, urgency & category breakdown.
- 🚨 **Urgency + sentiment detection** — escalations flagged before the refund.
- 🔁 **AI follow-ups** — tone escalates by reminder count.
- 📜 **Activity feed** — every operational event, audit-trail style.
- 🎯 **Status lifecycle** — `pending` → `paid` / `overdue` / `failed` with webhook simulator.

**Bonus**
- Retry-safe Anthropic client with structured-JSON parsing.
- Heuristic fallback so the demo runs without an API key.
- Request-id logging middleware.
- Docker + docker-compose one-command boot.
- Postgres-shaped mock DB for trivial migration.
- Vercel + Render deployment configs.

## 9. Scalability Roadmap

| Area | Today (MVP) | Next |
|---|---|---|
| **Payments** | Mock link mint | Real Nomod link API, idempotent mint, ledger reconciliation |
| **Webhooks** | `POST /webhook/paid` simulator | Provider signatures, retries, DLQ |
| **Queues** | In-process | Arq / Celery on Redis, scheduled follow-up cadence |
| **Events** | JSON store activity log | Event-driven (Kafka / SQS), per-event handlers |
| **Observability** | Request-id logging | OpenTelemetry traces, Grafana dashboards, AI-call cost telemetry |
| **Fraud** | None | Velocity + anomaly scoring before mint, sentiment-weighted risk |
| **Agents** | Two AI calls (extract, draft) | Supervised multi-agent — `extractor`, `dunning`, `recon`, `risk` |
| **Languages** | English | Arabic, mixed-code (UAE-style), per-merchant locale |
| **Auth** | `merchant_id` threaded end-to-end | JWT + RBAC, merchant org model |

## 10. Engineering Philosophy

> I intentionally focused on **rapid MVP execution with scalable modular architecture and AI-native workflow design rather than overengineering.**

Every layer is the smallest credible version of the production system:

- The mock DB matches the Postgres schema, so the migration is mechanical.
- The Claude client is one file with retry, JSON parsing, and a fallback — small enough to read in 60 seconds, structured enough to extend.
- Services are pure functions over the store — trivial to unit-test, trivial to swap to real Nomod APIs.
- The UI prioritises **operational density** (cards, badges, activity feed) over decorative chrome. It looks like fintech ops software, not a chatbot demo.

The goal: something an AI-native startup engineer would prototype on day one, ship to a real merchant on day three, and harden into production by week two.

## 11. Local Setup

### Docker (recommended)

```bash
cp .env.example .env       # add ANTHROPIC_API_KEY (optional — fallback works)
docker compose up --build
# Frontend → http://localhost:3000
# Backend  → http://localhost:8000/docs
```

### Native dev

```bash
./scripts/start.sh
# or, manually:
cd backend && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000
cd ../frontend && npm install && npm run dev
```

## 12. Deployment

- **Frontend → Vercel** — `vercel.json` included. Root = `frontend/`, output = `dist/`.
- **Backend → Render** — `render.yaml` blueprint included. One-click from the dashboard.
- Full step-by-step: [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

## 13. API Docs

OpenAPI live at `/docs` once the backend is running.

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/ai/chat` | NL request → extraction + payment + WhatsApp draft |
| `GET` | `/api/payments` | List merchant payments |
| `GET` | `/api/payments/{id}` | Single payment |
| `PATCH` | `/api/payments/{id}/status` | Update status |
| `POST` | `/api/payments/{id}/followup` | Generate AI follow-up |
| `POST` | `/api/payments/{id}/webhook/paid` | Simulated provider webhook |
| `GET` | `/api/dashboard/metrics` | KPIs, volume, breakdowns |
| `GET` | `/api/dashboard/activity` | Recent activity feed |
| `GET` | `/health` | Liveness probe |

### Sample curl

```bash
curl -X POST http://localhost:8000/api/ai/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Charge Ahmed 500 AED for AC repair, urgent"}'
```

## 14. Future Improvements

- Native Arabic + mixed-code (English/Arabic) prompt + UI locale.
- Multi-agent supervisor: `extractor → risk → dunning → recon`.
- Per-merchant memory (RAG over past invoices, customer tone history).
- Apple Pay / Google Pay / Tabby / Tamara handoff inside the link mint.
- Slack / WhatsApp Business webhook ingress so the merchant never leaves their chat.
- Realtime collaboration when a merchant has multiple ops staff.

---

<div align="center">

**Built for the Nomod Product Engineer (AI-Native) interview.**
[Architecture diagrams](docs/architecture/) · [Deployment guide](docs/DEPLOYMENT.md) · [Demo script](docs/DEMO_SCRIPT.md)

</div>
