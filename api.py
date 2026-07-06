"""Demo API — same shape as the production service, backed by inline sample
data instead of a real catalog + trained models (those live in a private repo).
"""
import hmac
import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

API_KEY = os.environ.get("API_SHARED_KEY", "")
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "https://yourdomain.com")

DEMO_CATALOG = {
    "Hot Rolled Rounds": [
        {"index": 0, "label": "0.25", "dim1": 0.25, "dim2": None, "dim3": None,
         "weight_per_ft": 1.67, "stock_len_ft": 20, "shape_key": "ROUND BAR"},
        {"index": 1, "label": "0.5", "dim1": 0.5, "dim2": None, "dim3": None,
         "weight_per_ft": 6.68, "stock_len_ft": 20, "shape_key": "ROUND BAR"},
    ],
    "Square Tubing": [
        {"index": 0, "label": "2 X 2 x 0.120", "dim1": 2.0, "dim2": 2.0, "dim3": 0.12,
         "weight_per_ft": 3.07, "stock_len_ft": 20, "shape_key": "TUBE"},
    ],
}


def require_api_key(x_api_key: str = Header(default="")):
    if not API_KEY or not hmac.compare_digest(x_api_key, API_KEY):
        raise HTTPException(status_code=401, detail="invalid or missing API key")


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET", "POST"],
    allow_headers=["X-API-Key", "Content-Type"],
)


class PredictRequest(BaseModel):
    category: str
    item_index: int
    quantity: int
    length_ft: float
    is_domestic: bool = False


@app.get("/api/categories", dependencies=[Depends(require_api_key)])
def categories():
    return {"categories": list(DEMO_CATALOG.keys())}


@app.get("/api/items", dependencies=[Depends(require_api_key)])
def items(category: str):
    if category not in DEMO_CATALOG:
        raise HTTPException(400, f"unknown category: {category}")
    return {"items": DEMO_CATALOG[category]}


@app.post("/api/predict", dependencies=[Depends(require_api_key)])
def predict(req: PredictRequest):
    if req.quantity <= 0 or req.length_ft <= 0:
        raise HTTPException(400, "quantity and length_ft must be positive")
    entries = DEMO_CATALOG.get(req.category)
    if entries is None or not (0 <= req.item_index < len(entries)):
        raise HTTPException(400, "unknown category or item_index")

    item = entries[req.item_index]
    total_weight = round(item["weight_per_ft"] * req.length_ft * req.quantity, 2)
    price_per_lb = 1.15  # placeholder — real prediction model is not in this repo
    return {
        "category": req.category, "label": item["label"], "shape": item["shape_key"],
        "quantity": req.quantity, "length_ft": req.length_ft,
        "total_weight_lbs": total_weight,
        "price_per_lb": price_per_lb,
        "line_total": round(price_per_lb * total_weight, 2),
    }
