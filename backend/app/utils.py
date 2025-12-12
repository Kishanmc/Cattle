# backend/app/utils.py
from PIL import Image
import io
import numpy as np
from typing import Tuple

def preprocess_disease(img_bytes: bytes, input_shape: Tuple[int,int,int]):
    """
    Resize and normalize image to model input shape.
    input_shape: (H, W, C)
    """
    H, W, C = input_shape
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = img.resize((W, H))
    arr = np.array(img).astype("float32") / 255.0
    # expand batch dim
    return np.expand_dims(arr, 0)
