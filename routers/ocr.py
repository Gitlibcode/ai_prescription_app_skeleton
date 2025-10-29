from PIL import Image
import io

@router.post("/process_prescription")
async def process_prescription(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Please upload a JPG or PNG image.")

    content = await file.read()

    try:
        pil_image = Image.open(io.BytesIO(content)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Image decoding failed.")

    img = np.array(pil_image)
    print("📸 Image shape:", img.shape)

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
