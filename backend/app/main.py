# backend/app/main.py
import sys
from pathlib import Path

# Ensure backend folder is on sys.path so package imports resolve correctly
# This helps when uvicorn's reloader spawns subprocesses on Windows.
ROOT = Path(__file__).resolve().parents[1]  # backend/app -> backend
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import breed, disease, crossbreed


app = FastAPI(title="Cattle Vision API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(breed.router, prefix="/predict_breed", tags=["breed"])
app.include_router(disease.router, prefix="/predict_disease", tags=["disease"])
app.include_router(crossbreed.router, prefix="/predict_crossbreed", tags=["crossbreed"])
