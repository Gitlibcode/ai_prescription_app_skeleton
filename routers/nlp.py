from fastapi import APIRouter

router = APIRouter(prefix="/nlp", tags=["NLP"])

@router.post("/extract_salts")
async def extract_salts(text: str):
    return {"msg": "NLP salt extraction placeholder", "salts": []}