import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io

CLASS_NAMES = ["ayshire", "brown_swiss", "holstein", "jersey", "RedDane"]

class EnhancedCattleClassifier(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.backbone = models.efficientnet_b3(weights=None)
        feature_dim = self.backbone.classifier[1].in_features
        self.backbone.classifier = nn.Identity()
        self.classifier = nn.Sequential(
            nn.Linear(feature_dim, 1024),
            nn.BatchNorm1d(1024),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(1024, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        x = self.backbone(x)
        x = self.classifier(x)
        return x

def get_transform():
    return transforms.Compose([
        transforms.Resize(300),
        transforms.CenterCrop(300),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])

def load_model(checkpoint_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    ckpt = torch.load(checkpoint_path, map_location=device)
    if isinstance(ckpt, dict) and "model_state_dict" in ckpt:
        state_dict = ckpt["model_state_dict"]
    else:
        state_dict = ckpt
    model = EnhancedCattleClassifier(num_classes=len(CLASS_NAMES))
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    transform = get_transform()
    return model, device, transform

def predict_bytes(model, device, transform, image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    x = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(x)
        probs = torch.softmax(logits, dim=1)[0]
    conf, idx = torch.max(probs, dim=0)
    idx = idx.item()
    label = CLASS_NAMES[idx] if idx < len(CLASS_NAMES) else str(idx)
    return label, float(conf.item()), probs.cpu().tolist()
