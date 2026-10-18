# backend/app/api/crossbreed.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.concurrency import run_in_threadpool

from ..core.model_loader import models
from ..static_data import BREED_STATIC_DATA
from .. import cattle_model

router = APIRouter()

@router.post("/", response_model=dict)
async def predict_crossbreed(
    parent_a: UploadFile = File(...),
    parent_b: UploadFile = File(...),
):
    # validate content types
    if not parent_a.content_type.startswith("image/") or not parent_b.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Both files must be images.")

    a_bytes = await parent_a.read()
    b_bytes = await parent_b.read()

    try:
        # ensure breed model loaded
        breed_model, breed_device, breed_transform = models.load_breed()

        # import predict function from cattle_model in runtime to avoid startup circular issues
        from app import cattle_model

        def _pred(bytes_):
            return cattle_model.predict_bytes(breed_model, breed_device, breed_transform, bytes_)

        # run both predictions off event loop
        a_label, a_conf, a_extra = await run_in_threadpool(lambda: _pred(a_bytes))
        b_label, b_conf, b_extra = await run_in_threadpool(lambda: _pred(b_bytes))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crossbreed prediction failed: {e}")

    # normalize keys for static lookup
    a_static = BREED_STATIC_DATA.get(a_label.lower(), {})
    b_static = BREED_STATIC_DATA.get(b_label.lower(), {})

    # Simple crossbreed logic (example): combine names and provide basic static info.
    # You can change this to your domain logic: e.g., map pair -> expected hybrid characteristics.
    cross_name = f"{a_label} x {b_label}"

    # Example heuristics for combined fields (you can make this more complex or load from a crossbreed DB)
    def combine_field(field):
        a_val = a_static.get(field)
        b_val = b_static.get(field)
        if a_val and b_val:
            # if numeric-like strings exist you might want to parse; for now prefer first then second
            return f"{a_val} / {b_val}"
        return a_val or b_val or "N/A"

    hybrid_info = {
        "cross_name": cross_name,
        "expected_milk_type": combine_field("milk_type"),
        "expected_average_milk_yield": combine_field("average_milk_yield"),
        "expected_primary_color": combine_field("primary_color"),
        "expected_size": combine_field("size"),
        "expected_temperament": combine_field("temperament"),
        "notes": f"Parent A: {a_label} ({a_conf:.2f}), Parent B: {b_label} ({b_conf:.2f}).",
    }

    return {
        "parent_a": {"filename": parent_a.filename, "predicted_class": a_label, "confidence": float(a_conf), "static_data": a_static},
        "parent_b": {"filename": parent_b.filename, "predicted_class": b_label, "confidence": float(b_conf), "static_data": b_static},
        "crossbreed": hybrid_info
    }
