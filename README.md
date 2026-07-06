# Steel Price Estimator (demo)

A small catalog-driven price estimator: pick a category, pick an item, enter
quantity and length, get a predicted $/lb and line total.

This is a **showcase repo** — the API here (`api.py`) mirrors the real
service's routes, auth, and CORS setup, but runs on inline sample data with a
fixed placeholder price instead of the actual trained pricing model. The real
catalog and model logic are kept in a private repo.

## Structure

- `web/index.html` — static frontend, no build step
- `api.py` — FastAPI backend: `/api/categories`, `/api/items`, `/api/predict`

## Run locally

```
pip install fastapi "uvicorn[standard]"
API_SHARED_KEY=your-key ALLOWED_ORIGIN=http://localhost:8080 uvicorn api:app --reload --port 8000
```

Set the same key as `KEY` in `web/index.html`, then serve `web/` with any
static file server and open it in a browser.
