# Hero API - Week 9 PostgreSQL and SQLModel Lab

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DATABASE_URL = "postgresql+psycopg://hero_app:YOUR_PASSWORD@127.0.0.1:5432/hero_app_db"
```

Start the API:

```powershell
fastapi dev app/main.py
```

Open `http://127.0.0.1:8000/docs` to exercise the endpoints.

## Week 9 migration lifecycle

The tracked migration is the Part 9 historical change that adds `hero.power`
to the pre-existing tables created earlier in the lab. On the lab database,
apply it with:

```powershell
alembic upgrade head
```

Then add the sample data:

```powershell
python -m app.seed
```

The seed command is idempotent: it leaves an already seeded database untouched.
