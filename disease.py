"""
Disease Detection Module for Cattle
Provides functions for loading and predicting cattle diseases using TensorFlow model.
"""

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io
from typing import Tuple, List

CLASS_NAMES = ["IBK", "FMD", "LSD"]
MODEL_PATH = "custom_model.h5"


def load_disease_model(model_path: str = MODEL_PATH):
    """
    Load the disease detection model and get input dimensions.
    
    Args:
        model_path: Path to the .h5 model file
        
    Returns:
        Tuple of (model, height, width, channels)
    """
    model = load_model(model_path)
    _, h, w, c = model.input_shape
    print(f"Model loaded. Expected input size: {h}x{w}x{c}")
    return model, h, w, c


def preprocess_image_from_path(img_path: str, target_size: Tuple[int, int]) -> np.ndarray:
    """
    Load and preprocess an image from file path.
    
    Args:
        img_path: Path to the image file
        target_size: Tuple of (height, width)
        
    Returns:
        Preprocessed image array ready for prediction
    """
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array


def preprocess_image_from_bytes(img_bytes: bytes, target_size: Tuple[int, int]) -> np.ndarray:
    """
    Load and preprocess an image from bytes.
    
    Args:
        img_bytes: Image data as bytes
        target_size: Tuple of (height, width)
        
    Returns:
        Preprocessed image array ready for prediction
    """
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, 0)


def predict_disease(model, img_array: np.ndarray, class_names: List[str] = CLASS_NAMES) -> Tuple[str, float, np.ndarray]:
    """
    Predict disease from preprocessed image array.
    
    Args:
        model: Loaded Keras model
        img_array: Preprocessed image array
        class_names: List of class names
        
    Returns:
        Tuple of (predicted_class_name, confidence, prediction_probabilities)
    """
    pred = model.predict(img_array, verbose=0)
    class_id = np.argmax(pred)
    confidence = float(np.max(pred))
    predicted_class = class_names[class_id]
    
    return predicted_class, confidence, pred[0]


def main():
    """Example usage of the disease detection module."""
    # 1. Load model
    model, h, w, c = load_disease_model()
    
    # 2. Load and preprocess image
    img_path = "image.png"  # Replace with your image path
    
    try:
        img_array = preprocess_image_from_path(img_path, target_size=(h, w))
        
        # 3. Predict
        predicted_class, confidence, probabilities = predict_disease(model, img_array)
        
        # 4. Display results
        print(f"\nPredicted Class: {predicted_class}")
        print(f"Confidence: {confidence:.2%}")
        print(f"\nClass Probabilities:")
        for i, class_name in enumerate(CLASS_NAMES):
            print(f"  {class_name}: {probabilities[i]:.2%}")
            
    except FileNotFoundError:
        print(f"Error: Image file '{img_path}' not found.")
        print("Please provide a valid image path.")
    except Exception as e:
        print(f"Error during prediction: {str(e)}")


if __name__ == "__main__":
    main()
