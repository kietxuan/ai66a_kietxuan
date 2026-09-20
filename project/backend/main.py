from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="Mini FastAPI Lab API", version="1.0.0")


# Lab 1-2: in-memory items CRUD
class ItemCreate(BaseModel):
    name: str
    price: float


class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None


class ItemPublic(BaseModel):
    id: int
    name: str
    price: float


class ItemListResponse(BaseModel):
    items: list[ItemPublic]
    total: int
    skip: int
    limit: int


_items: list[ItemPublic] = []
_next_id = 1


def find_item(item_id: int) -> ItemPublic | None:
    return next((item for item in _items if item.id == item_id), None)


def ensure_unique_name(name: str, current_id: int | None = None) -> None:
    duplicate = any(
        item.name.casefold() == name.casefold() and item.id != current_id
        for item in _items
    )
    if duplicate:
        raise HTTPException(
            status_code=409,
            detail="Item with this name already exists",
        )


@app.get("/items", response_model=ItemListResponse)
def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    min_price: float | None = None,
    max_price: float | None = None,
    q: str | None = Query(None, min_length=2),
    sort_by: str = Query("id", pattern="^(id|name|price)$"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
):
    filtered_items = _items

    if min_price is not None:
        filtered_items = [item for item in filtered_items if item.price >= min_price]
    if max_price is not None:
        filtered_items = [item for item in filtered_items if item.price <= max_price]
    if q is not None:
        search_text = q.casefold()
        filtered_items = [
            item for item in filtered_items if search_text in item.name.casefold()
        ]

    filtered_items = sorted(
        filtered_items,
        key=lambda item: getattr(item, sort_by),
        reverse=order == "desc",
    )

    return {
        "items": filtered_items[skip : skip + limit],
        "total": len(filtered_items),
        "skip": skip,
        "limit": limit,
    }


@app.post("/items", response_model=ItemPublic, status_code=201)
def create_item(data: ItemCreate):
    global _next_id

    ensure_unique_name(data.name)
    item = ItemPublic(id=_next_id, **data.model_dump())
    _items.append(item)
    _next_id += 1
    return item


@app.get("/items/{item_id}", response_model=ItemPublic)
def get_item(item_id: int):
    item = find_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=ItemPublic)
def replace_item(item_id: int, data: ItemCreate):
    item = find_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    if data.name.casefold() != item.name.casefold():
        ensure_unique_name(data.name, current_id=item_id)

    updated_item = ItemPublic(id=item_id, **data.model_dump())
    _items[_items.index(item)] = updated_item
    return updated_item


@app.patch("/items/{item_id}", response_model=ItemPublic)
def update_item(item_id: int, data: ItemUpdate):
    item = find_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    changes = data.model_dump(exclude_unset=True)
    if "name" in changes and changes["name"].casefold() != item.name.casefold():
        ensure_unique_name(changes["name"], current_id=item_id)

    updated_item = ItemPublic(**(item.model_dump() | changes))
    _items[_items.index(item)] = updated_item
    return updated_item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    item = find_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    _items.remove(item)
    return Response(status_code=204)


# Lab 3: existing house-price project integration
@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse(url="/static/house_form.html")


def predict_price(area: float, bedrooms: int, location: str) -> float:
    price = 500_000_000
    price += 15_000_000 * area
    price += 50_000_000 * bedrooms

    normalized_location = location.strip().lower()
    if normalized_location == "hanoi":
        price *= 1.3
    elif normalized_location == "hcmc":
        price *= 1.25

    return float(int(price / 1_000_000 + 0.5) * 1_000_000)


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
    predicted_price = predict_price(house.area, house.bedrooms, house.location)
    return {
        "area": house.area,
        "bedrooms": house.bedrooms,
        "location": house.location,
        "predicted_price": predicted_price,
    }


# Extra practice: body validation and a separate prediction endpoint.
class HousePriceRequest(BaseModel):
    area_sqm: float = Field(gt=0)
    bedrooms: int = Field(ge=0)
    distance_to_center_km: float


class HousePricePrediction(BaseModel):
    predicted_price: float
    currency: str = "VND"


@app.post("/predict/house-price", response_model=HousePricePrediction)
def predict_house_price(house: HousePriceRequest):
    predicted_price = (
        house.area_sqm * 15_000_000
        - house.distance_to_center_km * 5_000_000
        + house.bedrooms * 20_000_000
    )
    return HousePricePrediction(predicted_price=predicted_price)


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
