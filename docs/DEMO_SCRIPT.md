# Loom Demo Script — 75 seconds

**Tone:** confident founder, AI-native, practical. No fluff. Eye on camera, fast cuts between screens.

---

### 0:00 — 0:10 · The problem (10 s)

> "UAE merchants live in WhatsApp. They make money in WhatsApp. But every charge — every link, every invoice, every follow-up — is hand-typed on a phone. That's hours a week, and it's where cash leaks."

🎬 Screen: WhatsApp chat with a half-written invoice; cut to a stack of unpaid links.

### 0:10 — 0:25 · The product, in one sentence (15 s)

> "So I built **Nomod AI** — a merchant operations agent. The merchant types one sentence. The agent does the rest."

🎬 Screen: Assistant page. Type:
> *Charge Ahmed 500 AED for AC repair, urgent.*

Press Generate. Card appears.

### 0:25 — 0:40 · AI extraction (15 s)

> "Under the hood, Claude turns that into a typed payment intent — customer, amount, urgency, sentiment, escalation. I parse strict JSON with Pydantic, and there's a deterministic fallback so the demo never breaks."

🎬 Screen: hover the card — badges visible (urgency, escalation). Cut to `extractor.py` for half a second to show the structured output.

### 0:40 — 0:55 · Payment workflow (15 s)

> "It mints a Nomod-style link, drafts the WhatsApp message in the right tone, and starts the lifecycle. When the customer pays, a webhook updates status. If they don't, the agent writes a follow-up — gentle the first time, urgent by the third."

🎬 Screen: click **Mark paid** → status flips to green. Then on another card, click **AI follow-up** → message appears.

### 0:55 — 1:05 · Ops dashboard (10 s)

> "Every event lands in the activity feed. Collection rate, escalations, urgency mix — all live."

🎬 Screen: Analytics tab. Pan across the KPIs.

### 1:05 — 1:15 · The scaling story (10 s)

> "Today it's a single agent and a mock store. The architecture is built for what's next — multi-agent supervision, real webhook signing, Postgres, fraud scoring, Arabic. The mock DB has the same shape as the production schema. The Claude client is one file. Swap, don't rewrite."

🎬 Screen: split-view — `docs/architecture/architecture-diagram.md` rendered.

### Closing (3 s)

> "Built end-to-end for the Nomod Product Engineer role. Chat to paid in seconds."

🎬 Screen: README hero.

---

## Recording checklist

- [ ] 1440 × 900 window, dock hidden, dark mode
- [ ] Run 4 suggestion chips before recording so KPIs aren't zero
- [ ] Mark one payment paid + one with a follow-up before record start
- [ ] Speak in present tense, no "let me show you" filler
- [ ] Loom title: **"Nomod AI — Chat to Paid in Seconds (Product Engineer submission)"**
