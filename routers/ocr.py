from fastapi import APIRouter, UploadFile, File, HTTPException
import numpy as np
import cv2
from PIL import Image
import io
from paddleocr import PaddleOCR
from pdf import extract_text_from_pdf
from nlp import extract_salts
from rag import get_prices

router = APIRouter()

def get_ocr():
    return PaddleOCR(use_angle_cls=True, lang='en')

def should_run_ocr(filename: str) -> bool:
    return filename.lower().endswith((".jpg", ".jpeg", ".png"))

@router.post("/process_prescription")
async def process_prescription(file: UploadFile = File(...)):
    filename = file.filename.lower()
    content = await file.read()

    if should_run_ocr(filename):
        try:
            pil_image = Image.open(io.BytesIO(content)).convert("RGB")
        except Exception:
            raise HTTPException(status_code=400, detail="Image decoding failed.")

        img = np.array(pil_image)
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        ocr = get_ocr()
        result = ocr.ocr(img)
        lines = [line[1][0] for res in result for line in res]
        extracted_text = " ".join(lines)

    else:
        try:
            extracted_text = extract_text_from_pdf(content)
        except Exception:
            raise HTTPException(status_code=400, detail="PDF text extraction failed.")

    nlp_result = await extract_salts(extracted_text)
    salts = nlp_result.get("salts", [])

    rag_result = await get_prices(salts)
    prices = rag_result.get("prices", {})

    return {
        "msg": "✅ File processed successfully",
        "filename": filename,
        "extracted_text": extracted_text.strip(),
        "salts": salts,
        "prices": prices
    }
