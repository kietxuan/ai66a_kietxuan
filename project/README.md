# House Price Prediction API

This project connects the Week 2 house form to a FastAPI backend. It includes a synchronous `predict_price()` function, `GET /predict`, `POST /predict`, and the frontend served by FastAPI from the same origin. The frontend is split into `house_form.html`, `style.css`, and `app.js`.

## How to run

From PowerShell, run these commands in order:

```powershell
cd project
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cd backend
uvicorn main:app --reload
```

Run `python -m venv venv` only the first time, or whenever the virtual environment needs to be recreated. If PowerShell blocks activation, run Uvicorn without activating the environment:

```powershell
cd backend
..\venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open the form at:

`http://127.0.0.1:8000/static/house_form.html`

You can also open the shorter URL below; it redirects to the form:

`http://127.0.0.1:8000/`

The interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

## Required checks and explanations

For `GET /predict?area=80&bedrooms=3&location=hanoi`, the returned JSON is:

```json
{
  "area": 80.0,
  "bedrooms": 3,
  "location": "hanoi",
  "predicted_price": 2405000000.0
}
```

- `location` is optional, so omitting it still works because FastAPI uses the default value `"other"`.
- `area` is required, so omitting it returns HTTP `422`: FastAPI validates the typed query parameters before calling the endpoint.
- The endpoints use `def` because the calculation is short and synchronous; there is no asynchronous I/O to await.
- A query parameter is sent in the URL, while the POST endpoint receives the fields inside a JSON request body.
- The frontend uses the relative URL `/predict`. Because FastAPI serves the page and API on `127.0.0.1:8000`, the browser sends the request to the same origin and no CORS configuration is needed.

The browser form formats the returned `predicted_price` with thousands separators and displays an error message if the API request fails.
