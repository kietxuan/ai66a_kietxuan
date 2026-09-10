from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Mini House-Price Prediction API", version="1.0.0")


@app.get("/", include_in_schema=False)
def home():
    """Open the house-price form when the server root is visited."""
    return RedirectResponse(url="/static/house_form.html")


def predict_price(area: float, bedrooms: int, location: str) -> float:
    """Return a simplified house-price prediction in VND."""
    price = 500_000_000
    price += 15_000_000 * area
    price += 50_000_000 * bedrooms

    normalized_location = location.strip().lower()

    if normalized_location == "hanoi":
        price *= 1.3
    elif normalized_location == "hcmc":
        price *= 1.25

    price = int(price / 1_000_000 + 0.5) * 1_000_000
    return float(price)


# This endpoint uses def because the calculation is synchronous and does not need async I/O.
@app.get("/predict")
def get_prediction(area: float, bedrooms: int, location: str = "other"):
    predicted_price = predict_price(area, bedrooms, location)

    return {
        "area": area,
        "bedrooms": bedrooms,
        "location": location,
        "predicted_price": predicted_price,
    }


class HouseInput(BaseModel):
    area: float
    bedrooms: int
    location: str = "other"


@app.post("/predict")
def post_prediction(house: HouseInput):
    predicted_price = predict_price(
        house.area,
        house.bedrooms,
        house.location,
    )

    return {
        "area": house.area,
        "bedrooms": house.bedrooms,
        "location": house.location,
        "predicted_price": predicted_price,
    }


# Resolve the frontend relative to this file so the mount works from any current directory.
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
