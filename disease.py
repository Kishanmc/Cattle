from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# 1. Load model
model = load_model("custom_model.h5")   # or your .h5 file name

# 2. Get input size dynamically
_, h, w, c = model.input_shape   # e.g. (None, 64, 64, 3)
print("Model expects input size:", h, "x", w, "x", c)

class_names = ["IBK", "FMD", "LSD"]

# 3. Load and preprocess image
img_path = "image.png"

img = image.load_img(img_path, target_size=(h, w))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = img_array / 255.0

# 4. Predict
pred = model.predict(img_array)
class_id = np.argmax(pred)
confidence = float(np.max(pred))

print("Predicted Class:", class_names[class_id])
print("Confidence:", confidence)
