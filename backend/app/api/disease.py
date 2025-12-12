from fastapi import APIRouter, UploadFile, File, HTTPException
import numpy as np

from ..core.model_loader import models
from ..schemas import PredictionResponse
from ..static_data import DISEASE_STATIC_DATA, DISEASE_CLASS_NAMES
from ..utils import preprocess_disease


router = APIRouter()

@router.post("/", response_model=PredictionResponse)
async def predict_disease(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
    img_bytes = await file.read()

    try:
        disease_model, input_shape = models.load_disease()
        arr = preprocess_disease(img_bytes, input_shape)
        pred = disease_model.predict(arr)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Disease prediction failed: {e}")

    class_id = int(np.argmax(pred))
    label = DISEASE_CLASS_NAMES[class_id]
    conf = float(np.max(pred))
    static = DISEASE_STATIC_DATA.get(label, {})

    return {
        "filename": file.filename,
        "predicted_class": label,
        "confidence": conf,
        "static_data": static
    }
