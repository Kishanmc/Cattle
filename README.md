"# Cattle Vision AI 🐄

An AI-powered cattle breed classification and disease detection system using deep learning models.

## Features

### 🎯 Dual Classification Modes
- **Breed Classification**: Identifies 5 major dairy breeds (Ayrshire, Brown Swiss, Holstein, Jersey, Red Dane)
- **Disease Detection**: Detects 3 common cattle diseases (IBK, FMD, LSD)

### 🚀 Key Capabilities
- Upload images or use live camera feed
- Real-time prediction with confidence scores
- Detailed breed/disease information
- PDF report generation
- Responsive modern UI with dark/light theme
- Cross-browser compatible
- File validation and security checks

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PyTorch**: Breed classification using EfficientNet-B3
- **TensorFlow/Keras**: Disease detection CNN model
- **PIL/Pillow**: Image processing

### Frontend
- Pure HTML5, CSS3, JavaScript
- jsPDF for report generation
- Modern responsive design

## Installation

### Prerequisites
- Python 3.8+
- CUDA-compatible GPU (optional, for faster inference)

### Setup

1. **Clone or download the repository**

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn torch torchvision pillow numpy tensorflow
```

4. **Verify model files exist**
- `best_enhanced_model.pth` (Breed model)
- `custom_model.h5` (Disease model)

## Usage

### Starting the Server

```bash
python app.py
```

The server will start on `http://localhost:8000`

### Opening the Web Interface

1. Open `index.html` in a modern web browser
2. Or use a local server:
```bash
python -m http.server 8080
# Then open http://localhost:8080/index.html
```

### Making Predictions

**Method 1: Upload Image**
1. Click "Choose File" to select an image
2. Click "⚡ Predict from Image"
3. View results with detailed information

**Method 2: Use Camera**
1. Click "📷 Start Camera"
2. Allow camera permissions
3. Position the cattle in the frame
4. Click "🎯 Capture & Predict"

**Switching Modes**
- Click "🐄 Breed mode" for breed classification
- Click "🩺 Disease mode" for disease detection

## API Endpoints

### Health Check
```
GET /
GET /health
```

### Breed Prediction
```
POST /predict_breed
Content-Type: multipart/form-data
Body: file (image file)

Response:
{
  "filename": "cow.jpg",
  "predicted_class": "holstein",
  "confidence": 0.956,
  "static_data": { ... breed details ... }
}
```

### Disease Detection
```
POST /predict_disease
Content-Type: multipart/form-data
Body: file (image file)

Response:
{
  "filename": "cattle.jpg",
  "predicted_class": "FMD",
  "confidence": 0.892,
  "static_data": { ... disease details ... }
}
```

## File Structure

```
Cattle/
├── app.py                    # FastAPI backend server
├── cattle_model.py           # Breed classification model
├── disease.py                # Disease detection utilities
├── index.html                # Frontend web interface
├── best_enhanced_model.pth   # PyTorch breed model
├── custom_model.h5           # TensorFlow disease model
└── README.md                 # This file
```

## Recent Improvements

### Security & Validation
- ✅ File size limits (10MB max)
- ✅ File type validation (JPEG, PNG, WebP)
- ✅ Image dimension checks (4096px max)
- ✅ Image corruption detection
- ✅ Proper CORS configuration

### Error Handling
- ✅ User-friendly error messages
- ✅ Network error detection
- ✅ Comprehensive logging
- ✅ Validation feedback

### UI/UX Enhancements
- ✅ Viewport meta tag for mobile
- ✅ Accessible form labels
- ✅ Better loading states
- ✅ Camera error handling
- ✅ Browser compatibility fixes
- ✅ Dark/light theme toggle

### Code Quality
- ✅ Type hints in disease.py
- ✅ Comprehensive docstrings
- ✅ Modular function structure
- ✅ Better code organization

## Supported Breeds

1. **Ayrshire** - Hardy Scottish breed, excellent grazer
2. **Brown Swiss** - Ancient Alpine breed, ideal for cheese
3. **Holstein Friesian** - World's highest milk producer
4. **Jersey** - Premium dairy, high-fat milk
5. **Red Dane** - Robust Danish breed, great fertility

## Detectable Diseases

1. **FMD** (Foot-and-Mouth Disease) - Highly contagious viral disease
2. **IBK** (Infectious Bovine Keratoconjunctivitis/Pinkeye) - Bacterial eye infection
3. **LSD** (Lumpy Skin Disease) - Viral disease causing skin nodules

## Troubleshooting

### Server won't start
- Check if port 8000 is already in use
- Verify all dependencies are installed
- Ensure model files exist in the directory

### Predictions fail
- Verify the backend server is running
- Check image file format and size
- Ensure image is not corrupted
- Try a different image with better quality

### Camera not working
- Allow camera permissions in browser
- Use HTTPS or localhost
- Try a different browser (Chrome/Edge recommended)
- Use image upload as alternative

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ⚠️ playsinline attribute not supported in Firefox (camera may behave differently)

## Performance Tips

- Use images under 5MB for faster uploads
- Resize large images before uploading
- Use GPU for faster model inference
- Close unused tabs to free memory

## License

This project is for educational and research purposes.

## Disclaimer

This system is designed for educational and triage support only. It **cannot replace** a licensed veterinarian's diagnosis. Always consult with qualified veterinary professionals for accurate diagnosis and treatment.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

**Version**: 1.0.0  
**Last Updated**: December 2025" 
