from fastapi import APIRouter

from app.db.session import check_database

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    database_status = "ok" if await check_database() else "unavailable"
    return {"status": "ok", "database": database_status}
