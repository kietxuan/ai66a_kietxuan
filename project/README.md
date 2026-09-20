# FastAPI Labs

This simple project completes the Week 7 labs in one `main.py` file.

- Lab 1: in-memory CRUD for `/items`
- Lab 2: validation, separate request/response models, status codes, 404 errors, paging, filtering, sorting, duplicate-name checks, and a paginated response envelope
- Lab 3: serves the existing house-price frontend from `/static`
- Extra practice: `PATCH /items/{item_id}` and `POST /predict/house-price`

## Run

From PowerShell:

```powershell
cd project
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cd backend
uvicorn main:app --reload
```

Open these URLs:

- Frontend: `http://127.0.0.1:8000/`
- API documentation: `http://127.0.0.1:8000/docs`

## Main item routes

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/items` | List items with `skip`, `limit`, `min_price`, `max_price`, `q`, `sort_by`, and `order` |
| POST | `/items` | Create an item |
| GET | `/items/{item_id}` | Get one item |
| PUT | `/items/{item_id}` | Replace one item |
| PATCH | `/items/{item_id}` | Update only fields sent in the body |
| DELETE | `/items/{item_id}` | Delete one item |

`GET /items` returns `{ "items": [], "total": 0, "skip": 0, "limit": 10 }` when no items exist. Item names must be unique without regard to upper/lower case; duplicate requests return HTTP 409.

## Prediction routes

The existing frontend calls `GET /predict`. The separate practice endpoint below accepts a JSON body:

```json
POST /predict/house-price
{
  "area_sqm": 80,
  "bedrooms": 3,
  "distance_to_center_km": 5
}
```
