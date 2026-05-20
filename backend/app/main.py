from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes_ai, routes_dashboard, routes_payments
from app.config import settings
from app.database.db import db
from app.middleware.logging import RequestLoggingMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    db.load()
    yield
    db.flush()


app = FastAPI(
    title="Nomod AI — Merchant Operations API",
    description="AI-native payment operations for UAE merchants. Chat to paid in seconds.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(routes_ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(routes_payments.router, prefix="/api/payments", tags=["payments"])
app.include_router(routes_dashboard.router, prefix="/api/dashboard", tags=["dashboard"])


@app.get("/health", tags=["meta"])
async def health() -> dict:
    return {"status": "ok", "env": settings.app_env}


@app.get("/", tags=["meta"])
async def root() -> dict:
    return {
        "name": "Nomod AI",
        "tagline": "Chat to paid in seconds",
        "docs": "/docs",
    }
