from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
async def dashboard():
    return {"msg": "Admin dashboard placeholder"}