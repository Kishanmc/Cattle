import json
import os
from cattle_model import load_model, predict_bytes

# Load the model
checkpoint_path = "best_enhanced_model.pth"
model, device, transform = load_model(checkpoint_path)

# Predict for parentA.jpg
with open("parentA.jpg", "rb") as f:
    a_bytes = f.read()
a_label, a_conf, _ = predict_bytes(model, device, transform, a_bytes)

# Predict for parentB.jpg
with open("parentB.jpg", "rb") as f:
    b_bytes = f.read()
b_label, b_conf, _ = predict_bytes(model, device, transform, b_bytes)

print(f"Parent A predicted breed: {a_label} (confidence: {a_conf:.2f})")
print(f"Parent B predicted breed: {b_label} (confidence: {b_conf:.2f})")

# Load cross info
with open("breed_cross_info.json", "r") as f:
    cross_info = json.load(f)

# Get the cross info
key1 = f"{a_label} x {b_label}"
key2 = f"{b_label} x {a_label}"
if key1 in cross_info:
    info = cross_info[key1]
elif key2 in cross_info:
    info = cross_info[key2]
else:
    info = {
        "parents": [a_label, b_label],
        "estimated_milk_yield_l_per_year": None,
        "disease_resistance": "Unknown",
        "calf_size": "Unknown",
        "calf_temperament": "Unknown",
        "recommended_use_case": "General dairy",
        "notes": "No static mapping available for this parent pair."
    }

print("\nCrossbreeding static info:")
print(json.dumps(info, indent=2))
