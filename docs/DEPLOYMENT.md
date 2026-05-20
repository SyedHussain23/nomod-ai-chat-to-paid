# Deployment Guide

This repo is wired for a **Vercel (frontend) + Render (backend)** split. Both are free-tier compatible.

---

## 1. Backend → Render

Render blueprint is at [`render.yaml`](../render.yaml). It defines:

- A Docker web service from `backend/Dockerfile`
- Health-check on `/health`
- A 1 GB persistent disk mounted at `/app/data` so the mock JSON store survives restarts
- All env vars except `ANTHROPIC_API_KEY` (which you set in the dashboard)

### Steps

1. Push this repo to GitHub.
2. In Render → **New** → **Blueprint** → pick your repo. Render reads `render.yaml`.
3. Set `ANTHROPIC_API_KEY` in the service env vars (or skip — the heuristic fallback still works).
4. Deploy. Note the URL, e.g. `https://nomod-ai-backend.onrender.com`.
5. Verify: `curl https://<your-backend>.onrender.com/health` → `{"status":"ok",...}`.
6. OpenAPI: `https://<your-backend>.onrender.com/docs`.

> **Note:** the free Render tier sleeps after ~15 min of inactivity. First request after sleep takes ~30 s. Upgrade to Starter ($7/mo) for always-on.

---

## 2. Frontend → Vercel

Config: [`vercel.json`](../vercel.json).

### Steps

1. In Vercel → **Add New** → **Project** → import the repo.
2. **Framework preset:** Other (Vercel will pick up `vercel.json` automatically).
3. **Build command** and **output directory** are set in `vercel.json`. Don't override.
4. **Edit `vercel.json`** to point `/api/(.*)` rewrites at your real Render URL, e.g.
   ```json
   { "source": "/api/(.*)", "destination": "https://nomod-ai-backend.onrender.com/api/$1" }
   ```
5. Deploy. Note the URL, e.g. `https://nomod-ai.vercel.app`.

### Update backend CORS

Back in Render, update `CORS_ORIGINS`:

```
https://nomod-ai.vercel.app,https://<your-preview>.vercel.app
```

Trigger a redeploy.

---

## 3. Final live surface

| Surface | URL |
|---|---|
| Frontend | `https://nomod-ai.vercel.app` |
| Backend health | `https://nomod-ai-backend.onrender.com/health` |
| OpenAPI docs | `https://nomod-ai-backend.onrender.com/docs` |

(Replace with your own subdomains.)

---

## 4. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `CORS error` in browser console | Vercel domain not in `CORS_ORIGINS` | Update Render env, redeploy. |
| `502 Bad Gateway` on first request | Render free tier cold start | Wait ~30 s and retry, or upgrade plan. |
| Chat returns generic fallback text | `ANTHROPIC_API_KEY` not set | Set it in Render env vars and redeploy. |
| Frontend builds but `/api/*` 404s | `vercel.json` rewrite still points to placeholder | Edit `destination` to your Render URL. |
| Data resets between deploys | Disk not mounted, or fresh disk on new service | Confirm the `nomod-ai-data` disk in Render is attached. |

---

## 5. Production hardening checklist

- [ ] Replace MockDB with Postgres (SQLModel or SQLAlchemy 2.x) — schema is already shaped for it.
- [ ] Sign webhooks (HMAC) and verify on the `/webhook/paid` route.
- [ ] Add JWT auth — `merchant_id` is already threaded through every service.
- [ ] Wire OpenTelemetry traces (the request-id middleware is the hook point).
- [ ] Move follow-up scheduling to Arq + Redis.
- [ ] Add rate-limiting on `/api/ai/chat` (Claude calls are non-trivial cost).
- [ ] Pin Anthropic SDK version and add a model-rollover env switch.
