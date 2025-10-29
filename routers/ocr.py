import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, HTTPException
from paddleocr import PaddleOCR
import threading

router = APIRouter(prefix="/ocr", tags=["OCR"])

_ocr_lock = threading.Lock()
_ocr_model = None

def get_ocr():
    global _ocr_model
    with _ocr_lock:
        if _ocr_model is None:
            print("🚀 Initializing PaddleOCR model...")
            _ocr_model = PaddleOCR(lang='en', use_angle_cls=True)
        return _ocr_model

@router.post("/process_prescription")
async def process_prescription(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Please upload a JPG or PNG image.")

    content = await file.read()
    np_img = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="Image decoding failed.")

    print("📸 Image shape:", img.shape)
    print("📸 Image dtype:", img.dtype)

    # Optional: Resize to improve OCR accuracy
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    ocr = get_ocr()
    result = ocr.ocr(img)

    lines = [line[1][0] for res in result for line in res]

    return {
        "msg": "✅ OCR completed successfully",
        "filename": file.filename,
        "lines": lines,
        "line_count": len(lines),
        "extracted_text": " ".join(lines)
    }
