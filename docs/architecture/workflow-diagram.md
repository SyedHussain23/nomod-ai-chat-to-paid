# AI Workflow & Payment Lifecycle

## 1. AI Workflow Orchestration

```mermaid
sequenceDiagram
    autonumber
    participant M as Merchant
    participant FE as React UI
    participant API as FastAPI
    participant EX as extractor
    participant FU as followup
    participant CC as Claude
    participant DB as MockDB

    M->>FE: "Charge Ahmed 500 AED for AC repair"
    FE->>API: POST /api/ai/chat
    API->>EX: extract_payment_intent(text)
    EX->>CC: JSON-mode call (system + user)
    alt success
        CC-->>EX: structured JSON
    else failure / no key
        EX->>EX: heuristic regex fallback
    end
    EX-->>API: ExtractedRequest (typed)
    API->>FU: generate_whatsapp_message(extraction, link)
    FU->>CC: short-draft call
    CC-->>FU: WhatsApp text
    FU-->>API: message
    API->>DB: insert payment + activity log
    API-->>FE: ChatResponse {payment, extraction, ai_summary}
    FE-->>M: rendered payment card + activity update
```

Key properties:
- **Idempotent fallback** — every AI step has a deterministic backup so the demo never breaks.
- **Retry-safe** — `claude_client` wraps every call with bounded exponential backoff.
- **Auditable** — each step logs an activity event, building a free audit trail.

## 2. Payment Lifecycle

```mermaid
stateDiagram-v2
    [*] --> pending: AI extraction + link mint
    pending --> paid: webhook /webhook/paid
    pending --> overdue: scheduler (future) / manual
    pending --> failed: provider error / manual
    pending --> pending: AI follow-up (count++)
    overdue --> paid: late settlement
    paid --> [*]
    failed --> [*]

    note right of pending
      Each follow-up escalates tone:
      1 = gentle · 2 = firm · 3+ = urgent
    end note
```

## 3. Escalation Detection

```mermaid
flowchart TD
    A[Free-text request] --> B{Claude extraction}
    B --> C[sentiment ∈ neutral/satisfied/frustrated/at_risk]
    B --> D[escalation_required ∈ true/false]
    C -->|frustrated or at_risk| E[Badge: escalation]
    D -->|true| E
    E --> F[Activity event: escalation.flagged]
    F --> G[Dashboard KPI: escalations]
    F --> H[Future: human review queue]
```

This is the seed of the future risk/dunning multi-agent system — every signal we need is already structured on the payment record.
