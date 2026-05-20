from fastapi import APIRouter

from app.services import activity_service, analytics_service

router = APIRouter()


@router.get("/metrics", summary="Merchant analytics & KPIs")
async def metrics(merchant_id: str = "mch_demo") -> dict:
    return analytics_service.dashboard_metrics(merchant_id)


@router.get("/activity", summary="Recent merchant activity feed")
async def activity(merchant_id: str = "mch_demo", limit: int = 30) -> list[dict]:
    return activity_service.recent(limit=limit, merchant_id=merchant_id)
