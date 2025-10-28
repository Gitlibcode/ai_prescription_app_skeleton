HEAD
from paddleocr import PaddleOCR

# Initialize OCR model (English)
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Path to your test image
image_path = 'your_image.jpg'

# Run OCR
result = ocr.ocr(image_path, cls=True)

# Print

from paddleocr import PaddleOCR

# Initialize OCR model (English)
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Path to your test image
image_path = 'your_image.jpg'

# Run OCR
result = ocr.ocr(image_path, cls=True)

# Print
3b72bcfd (Initial commit - OCR app)
