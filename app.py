from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool
import uvicorn
import numpy as np
from PIL import Image
import io

# ============================================================
#  FASTAPI INITIALIZATION
# ============================================================

app = FastAPI(title="Cattle Vision AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
#  BREED MODEL (PyTorch)
# ============================================================

from cattle_model import load_model as load_breed_model
from cattle_model import predict_bytes as predict_breed_bytes
from cattle_model import CLASS_NAMES as BREED_CLASS_NAMES

BREED_CHECKPOINT = "best_enhanced_model.pth"

try:
    breed_model, breed_device, breed_transform = load_breed_model(BREED_CHECKPOINT)
except Exception as e:
    raise RuntimeError(f"Failed to load breed model: {e}")


# ============================================================
#  DISEASE MODEL (TensorFlow)
# ============================================================

from tensorflow.keras.models import load_model as load_tf_model

DISEASE_MODEL_PATH = "custom_model.h5"
DISEASE_CLASS_NAMES = ["IBK", "FMD", "LSD"]

try:
    disease_model = load_tf_model(DISEASE_MODEL_PATH)
    _, H, W, C = disease_model.input_shape
except Exception as e:
    raise RuntimeError(f"Failed to load disease model: {e}")


# ============================================================
#  STATIC INFORMATION — BREEDS
# ============================================================

BREED_STATIC_DATA = {
    "ayshire": {
        "breed": "Ayrshire",
        "origin": "Scotland",
        "milk_type": "Moderate fat, high quality",
        "average_milk_yield": "5,000–7,000 liters/year",
        "primary_color": "Red and white",
        "size": "Medium",
        "temperament": "Hardy, active grazer",
        "use_case": "Pasture-based dairy",
        "fun_fact": "Known for strong feet—excellent for grazing pastures.",
        "history": "Developed in Ayr, Scotland in the 18th century.",
        "cross_breeding": "Improves grazing efficiency & udder quality.",
        "future_potential": "Perfect for sustainable & low-input dairy farming."
    },

    "brown_swiss": {
        "breed": "Brown Swiss",
        "origin": "Switzerland",
        "milk_type": "Ideal for cheese, high protein",
        "average_milk_yield": "6,000–9,000 liters/year",
        "primary_color": "Brown with light muzzle",
        "size": "Large",
        "temperament": "Calm",
        "use_case": "Cheese and dairy farms",
        "fun_fact": "One of the world's oldest dairy breeds.",
        "history": "Originated in the Swiss Alps.",
        "cross_breeding": "Improves robustness and cheese yield quality.",
        "future_potential": "High tolerance to heat and stress."
    },

    "holstein": {
        "breed": "Holstein Friesian",
        "origin": "Netherlands",
        "milk_type": "Very high yield, lower fat",
        "average_milk_yield": "8,000–12,000+ liters/year",
        "primary_color": "Black & white pattern",
        "size": "Large",
        "temperament": "Calm",
        "use_case": "High-production dairy farms",
        "fun_fact": "World's highest milk-producing breed.",
        "history": "Selective breeding for milk yield for 100+ years.",
        "cross_breeding": "Boosts yield efficiency in mixed herds.",
        "future_potential": "Essential for precision dairy automation."
    },

    "jersey": {
        "breed": "Jersey",
        "origin": "Jersey Island",
        "milk_type": "High fat & protein",
        "average_milk_yield": "4,000–6,000 liters/year",
        "primary_color": "Fawn/light brown",
        "size": "Small",
        "temperament": "Alert & friendly",
        "use_case": "Ghee, butter, premium dairy",
        "fun_fact": "Milk appears golden due to beta-carotene.",
        "history": "Closed herd book since 1800s.",
        "cross_breeding": "Improves fat %, fertility, calving ease.",
        "future_potential": "Great for premium dairy startups."
    },

    "RedDane": {
        "breed": "Red Dane",
        "origin": "Denmark",
        "milk_type": "Balanced composition",
        "average_milk_yield": "6,000–8,000 liters/year",
        "primary_color": "Red",
        "size": "Medium-Large",
        "temperament": "Robust & adaptable",
        "use_case": "Health-focused dairy systems",
        "fun_fact": "Built for longevity and fertility.",
        "history": "Improved using European dairy lines.",
        "cross_breeding": "Boosts fertility and long life.",
        "future_potential": "Ideal for low-antibiotic dairy systems."
    }
}


# ============================================================
#  STATIC INFORMATION — DISEASES
# ============================================================

DISEASE_STATIC_DATA = {
    "FMD": {
        "name": "Foot-and-Mouth Disease",
        "severity": "High",
        "pathogen": "Aphthovirus",
        "symptoms": [
            "Blisters on mouth & feet",
            "Lameness",
            "High fever",
            "Severe drooling"
        ],
        "transmission": "Airborne, direct contact, equipment",
        "treatment": "Supportive only – no direct cure",
        "prevention": "Vaccination, isolation, biosecurity",
        "danger_level": "Extremely contagious"
    },

    "IBK": {
        "name": "Pinkeye (IBK)",
        "severity": "Medium",
        "pathogen": "Moraxella bovis",
        "symptoms": [
            "Red swollen eyes",
            "Light sensitivity",
            "Corneal ulcer",
            "Watery discharge"
        ],
        "transmission": "Flies, dust, environment",
        "treatment": "Antibiotics + eye protection",
        "prevention": "Fly control, sanitation",
        "danger_level": "Can cause permanent blindness"
    },

    "LSD": {
        "name": "Lumpy Skin Disease",
        "severity": "High",
        "pathogen": "Capripoxvirus",
        "symptoms": [
            "Hard skin nodules",
            "Fever",
            "Swollen lymph nodes",
            "Drop in milk production"
        ],
        "transmission": "Mosquitoes & biting flies",
        "treatment": "Supportive only",
        "prevention": "Vaccination & insect control",
        "danger_level": "Rapid farm-wide spread"
    },
}


# ============================================================
#  RESPONSE MODEL
# ============================================================

class PredictionResponse(BaseModel):
    filename: str
    predicted_class: str
    confidence: float
    static_data: dict


# ============================================================
#  IMAGE PREPROCESSING — DISEASE MODEL
# ============================================================

def preprocess_disease(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = img.resize((H, W))
    arr = np.array(img) / 255.0
    return np.expand_dims(arr, 0)


# ============================================================
#  ENDPOINT: BREED PREDICTION
# ============================================================

@app.post("/predict_breed", response_model=PredictionResponse)
async def predict_breed(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image.")

    content = await file.read()

    try:
        label, conf, _ = await run_in_threadpool(
            lambda: predict_breed_bytes(breed_model, breed_device, breed_transform, content)
        )
    except Exception as e:
        raise HTTPException(500, f"Breed prediction failed: {e}")

    static = BREED_STATIC_DATA.get(label.lower(), {})

    return {
        "filename": file.filename,
        "predicted_class": label,
        "confidence": float(conf),
        "static_data": static
    }


# ============================================================
#  ENDPOINT: DISEASE PREDICTION
# ============================================================

@app.post("/predict_disease", response_model=PredictionResponse)
async def predict_disease(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image.")

    img_bytes = await file.read()

    try:
        arr = preprocess_disease(img_bytes)
        pred = disease_model.predict(arr)[0]
    except Exception as e:
        raise HTTPException(500, f"Disease prediction failed: {e}")

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


# ============================================================
#  RUN SERVER
# ============================================================

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
