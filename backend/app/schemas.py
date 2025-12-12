# backend/app/schemas.py
from pydantic import BaseModel
from typing import Dict, Any

class PredictionResponse(BaseModel):
    filename: str
    predicted_class: str
    confidence: float
    static_data: Dict[str, Any]
