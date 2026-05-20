# Contributing

This is an interview submission, but the bar is real-product. If you're extending it, here's how the codebase wants to be touched.

## Ground rules

- **Small, scoped commits.** One concern per commit. The commit log is part of the product.
- **Services do logic. Routes do HTTP. AI does prompting.** Don't cross the lines.
- **No silent failures in AI calls.** Always log + fall back deterministically.
- **Pydantic at every boundary.** No raw dicts crossing an interface.
- **The mock DB is a Postgres rehearsal.** Don't shape the store in a way that won't translate.

## Dev loop

```bash
# Backend
cd backend && source .venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend && npm run dev
```

OpenAPI: http://localhost:8000/docs

## Adding a new AI step

1. Add the system prompt + a heuristic fallback in `backend/app/ai/<name>.py`.
2. Call it from a service, never directly from a route.
3. Log an activity event for every meaningful outcome.
4. Add a Pydantic schema for the return type — no `dict[str, Any]` leaks.

## Commit message style

```
<type>: <short imperative summary>

<body — optional, explains the why>
```

Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `perf`.

## Code review checklist

- Does the change preserve the AI fallback path?
- Does the change keep the request-id traceable end-to-end?
- Would this still work when we swap MockDB → Postgres?
- Is there a cheaper non-AI heuristic that fits the use case?
