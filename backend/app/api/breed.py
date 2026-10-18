# backend/app/api/breed.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.concurrency import run_in_threadpool

from ..core.model_loader import models
from ..schemas import PredictionResponse
from ..static_data import BREED_STATIC_DATA
from .. import cattle_model


router = APIRouter()

@router.post("/", response_model=PredictionResponse)
async def predict_breed(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
    content = await file.read()

    try:
        # ensure model loaded
        breed_model, breed_device, breed_transform = models.load_breed()
        # call blocking predict function off event loop
        def _predict():
            # cattle_model is expected to provide predict_bytes(model, device, transform, image_bytes)
            return models._breed, models._breed_device, models._breed_transform  # just to keep consistent loader

        # Use the cattle_model.predict_bytes implemented in your cattle_model.py
        # Import inside to avoid circular import issues at startup
        from app import cattle_model
        label, conf, extra = await run_in_threadpool(
            lambda: cattle_model.predict_bytes(breed_model, breed_device, breed_transform, content)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Breed prediction failed: {e}")

    static = BREED_STATIC_DATA.get(label.lower(), {})

    return {
        "filename": file.filename,
        "predicted_class": label,
        "confidence": float(conf),
        "static_data": static
    }
