# backend/app/core/model_loader.py
import os
from app import cattle_model
from tensorflow.keras.models import load_model as load_tf_model

# -------------------------------------------------
# Resolve backend/ directory safely
# -------------------------------------------------
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
# BASE_DIR -> reva/backend

BREED_MODEL_PATH = os.path.join(
    BASE_DIR, "models", "best_enhanced_model.pth"
)

DISEASE_MODEL_PATH = os.path.join(
    BASE_DIR, "models", "custom_model.h5"
)

class Models:
    def __init__(self):
        self._breed = None
        self._breed_device = None
        self._breed_transform = None
        self._disease = None
        self._disease_input_shape = None

    def load_breed(self):
        if self._breed is None:
            self._breed, self._breed_device, self._breed_transform = (
                cattle_model.load_model(BREED_MODEL_PATH)
            )
        return self._breed, self._breed_device, self._breed_transform

    def load_disease(self):
        if self._disease is None:
            self._disease = load_tf_model(DISEASE_MODEL_PATH)
            _, H, W, C = self._disease.input_shape
            self._disease_input_shape = (H, W, C)
        return self._disease, self._disease_input_shape

models = Models()
