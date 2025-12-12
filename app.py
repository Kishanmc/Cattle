from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool
import uvicorn
import numpy as np
from PIL import Image
import io
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
#  CONFIGURATION
# ============================================================

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_DIMENSION = 4096  # Maximum width or height
ALLOWED_EXTENSIONS = {"image/jpeg", "image/jpg", "image/png", "image/webp"}

# ============================================================
#  FASTAPI INITIALIZATION
# ============================================================

app = FastAPI(
    title="Cattle Vision AI",
    version="1.0.0",
    description="AI-powered cattle breed classification and disease detection system"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
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
#  IMAGE VALIDATION
# ============================================================

def validate_image_file(file: UploadFile, content: bytes) -> None:
    """Validate uploaded image file for security and format."""
    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, f"File size exceeds {MAX_FILE_SIZE // (1024*1024)}MB limit.")
    
    # Check content type
    if file.content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")
    
    # Validate it's actually an image
    try:
        img = Image.open(io.BytesIO(content))
        img.verify()
    except Exception as e:
        raise HTTPException(400, f"Invalid or corrupted image file: {str(e)}")
    
    # Check image dimensions
    img = Image.open(io.BytesIO(content))
    width, height = img.size
    if width > MAX_IMAGE_DIMENSION or height > MAX_IMAGE_DIMENSION:
        raise HTTPException(400, f"Image dimensions exceed maximum of {MAX_IMAGE_DIMENSION}px.")


# ============================================================
#  IMAGE PREPROCESSING — DISEASE MODEL
# ============================================================

def preprocess_disease(img_bytes):
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img = img.resize((H, W))
        arr = np.array(img) / 255.0
        return np.expand_dims(arr, 0)
    except Exception as e:
        logger.error(f"Disease preprocessing error: {e}")
        raise HTTPException(500, f"Failed to preprocess image: {str(e)}")


# ============================================================
#  HEALTH CHECK ENDPOINTS
# ============================================================

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Cattle Vision AI",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "breed_prediction": "/predict_breed",
            "disease_detection": "/predict_disease",
            "health_check": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "breed_model": "loaded",
        "disease_model": "loaded",
        "timestamp": np.datetime64('now').astype(str)
    }


# ============================================================
#  ENDPOINT: BREED PREDICTION
# ============================================================

@app.post("/predict_breed", response_model=PredictionResponse)
async def predict_breed(file: UploadFile = File(...)):
    """Predict cattle breed from uploaded image."""
    logger.info(f"Breed prediction requested for file: {file.filename}")
    
    # Read file content
    content = await file.read()
    
    # Validate image
    validate_image_file(file, content)

    try:
        label, conf, _ = await run_in_threadpool(
            lambda: predict_breed_bytes(breed_model, breed_device, breed_transform, content)
        )
        logger.info(f"Breed prediction successful: {label} ({conf:.2%})")
    except Exception as e:
        logger.error(f"Breed prediction failed: {str(e)}")
        raise HTTPException(500, f"Breed prediction failed: {str(e)}")

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
    """Detect cattle diseases from uploaded image."""
    logger.info(f"Disease prediction requested for file: {file.filename}")
    
    # Read file content
    img_bytes = await file.read()
    
    # Validate image
    validate_image_file(file, img_bytes)

    try:
        arr = preprocess_disease(img_bytes)
        pred = disease_model.predict(arr, verbose=0)[0]
    except Exception as e:
        logger.error(f"Disease prediction failed: {str(e)}")
        raise HTTPException(500, f"Disease prediction failed: {str(e)}")

    class_id = int(np.argmax(pred))
    label = DISEASE_CLASS_NAMES[class_id]
    conf = float(np.max(pred))
    
    logger.info(f"Disease prediction successful: {label} ({conf:.2%})")

    static = DISEASE_STATIC_DATA.get(label, {})

    return {
        "filename": file.filename,
        "predicted_class": label,
        "confidence": conf,
        "static_data": static
    }


# ============================================================
#  LIFECYCLE EVENTS
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    logger.info("="*50)
    logger.info("Cattle Vision AI - Starting up")
    logger.info(f"Breed model loaded: {BREED_CHECKPOINT}")
    logger.info(f"Disease model loaded: {DISEASE_MODEL_PATH}")
    logger.info(f"Breed classes: {', '.join(BREED_CLASS_NAMES)}")
    logger.info(f"Disease classes: {', '.join(DISEASE_CLASS_NAMES)}")
    logger.info("="*50)


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information."""
    logger.info("Cattle Vision AI - Shutting down")


# ============================================================
#  RUN SERVER
# ============================================================

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )