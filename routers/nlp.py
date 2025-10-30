from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

router = APIRouter(prefix="/nlp", tags=["NLP"])

# Load pre-trained medical NER model
model_name = "kamalkraj/bert-medical-ner"  # Good for medical entities
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Input format same as OCR output
class OCRInput(BaseModel):
    filename: str
    extracted_text: str

@router.post("/extract_salts")
async def extract_salts(data: OCRInput):
    text = data.extracted_text

    # Run NER on extracted text
    entities = ner_pipeline(text)

    # Filter relevant entities (MEDICINE, DOSAGE, FREQUENCY, DURATION)
    medicines: List[Dict] = []
    current_med = {}

    for ent in entities:
        label = ent["entity_group"].upper()
        word = ent["word"]

        if label in ["DRUG", "MEDICINE"]:
            if current_med:
                medicines.append(current_med)
                current_med = {}
            current_med["name"] = word
        elif label in ["STRENGTH", "DOSAGE"]:
            current_med["dosage"] = word
        elif label in ["FREQUENCY"]:
            current_med["frequency"] = word
        elif label in ["DURATION"]:
            current_med["duration"] = word

    if current_med:
        medicines.append(current_med)

    return {
        "msg": "✅ Medicines extracted using Transformer-based NLP",
        "filename": data.filename,
        "medicines": medicines
    }
