from fastapi import APIRouter, UploadFile, File, HTTPException
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".jfif", ".bmp", ".webp"}

@router.post("/")
async def upload_file(user_id: int, file: UploadFile = File(...)):
    # Log file details
    print(f"📁 Incoming file: {file.filename}, type: {file.content_type}")

    # Validate filename and extension
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Check extension
    ext = os.path.splitext(filename)[1].lower()
    print(f"🧩 File extension detected: {ext}")
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file type ({ext})")

    # Read file content
    contents = await file.read()
    file_size = len(contents)
    print(f"📏 File size: {file_size} bytes")

    # File size limit (20MB)
    if file_size > 20 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 20MB)")

    # Save locally
    file_path = os.path.join(UPLOAD_DIR, f"user_{user_id}_{filename}")
    with open(file_path, "wb") as f:
        f.write(contents)

    return {
        "msg": f"✅ File {filename} uploaded successfully",
        "saved_path": file_path,
        "file_size_bytes": file_size
    }
