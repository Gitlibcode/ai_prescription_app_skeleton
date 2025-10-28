import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, HTTPException
from paddleocr import PaddleOCR

router = APIRouter(prefix="/ocr", tags=["OCR"])

# Initialize OCR model once (outside the endpoint)
ocr = PaddleOCR(use_angle_cls=True, lang='en')

@router.post("/process_prescription")
async def process_prescription(file: UploadFile = File(...)):
    # ✅ Validate file type
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Please upload a JPG or PNG image.")

    # ✅ Read image bytes into OpenCV format
    content = await file.read()
    np_img = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # ✅ Run PaddleOCR
    result = ocr.ocr(img)

    # ✅ Extract text lines
    lines = [line[1][0] for res in result for line in res]

    return {
        "msg": "✅ OCR completed successfully",
        "filename": file.filename,
        "lines": lines,
        "line_count": len(lines),
        "extracted_text": " ".join(lines)
    }
