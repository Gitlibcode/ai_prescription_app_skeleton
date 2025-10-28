from fastapi import APIRouter

router = APIRouter(prefix="/delivery", tags=["Delivery"])

@router.post("/assign")
async def assign_delivery(order_id: int):
    return {"msg": "Delivery assignment placeholder", "order_id": order_id}