# System Architecture

End-to-end view of how a merchant request becomes a tracked payment.

```mermaid
flowchart LR
    subgraph Client["Merchant Browser"]
        UI[React + TS + Tailwind<br/>Assistant · Payments · Analytics]
    end

    subgraph API["FastAPI · async"]
        ROUTES["/api/ai · /api/payments · /api/dashboard"]
        MW[Request-ID + Logging middleware]
        SVC_P[payment_service]
        SVC_A[analytics_service]
        SVC_L[activity_service]
    end

    subgraph AI["AI Layer"]
        CC[claude_client<br/>retry · JSON parse · fallback]
        EX[extractor<br/>NL → typed intent]
        FU[followup<br/>tone-aware drafts]
    end

    subgraph Data["Storage"]
        DB[(MockDB<br/>Postgres-shaped)]
    end

    subgraph External
        AN[Anthropic API<br/>Claude 4.x]
        WH[Payment-provider<br/>webhook simulator]
    end

    UI -->|fetch /api/*| MW --> ROUTES
    ROUTES --> SVC_P --> EX --> CC --> AN
    SVC_P --> FU --> CC
    SVC_P --> DB
    SVC_P --> SVC_L --> DB
    ROUTES --> SVC_A --> DB
    WH -->|POST /webhook/paid| ROUTES
    SVC_A -->|KPIs| UI
    SVC_L -->|activity feed| UI
```

## Layer responsibilities

| Layer | Owns | Doesn't touch |
|---|---|---|
| **Routes** | HTTP schema, status codes, OpenAPI surface | Business logic, AI |
| **Services** | Domain logic, orchestration, store I/O | HTTP, prompt strings |
| **AI** | Prompt construction, retry, parsing, fallback | Persistence, HTTP |
| **Schemas** | Validation, OpenAPI types | I/O |
| **Database** | Persistence interface | Domain logic |

This separation is what lets us swap MockDB for Postgres, or swap Claude for a multi-agent router, without rewriting the routes or the frontend.
