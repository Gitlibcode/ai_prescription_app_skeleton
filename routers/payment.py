from fastapi import APIRouter

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/checkout")
async def checkout(order_id: int, amount: float):
    return {"msg": "Payment checkout placeholder", "order_id": order_id, "amount": amount}