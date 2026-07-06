# Steel Price Estimator (demo)

A small catalog-driven price estimator: pick a category, pick an item, enter
quantity and length, get a predicted $/lb and line total.

This is a **showcase repo**; the API here (`api.py`) mirrors the full
service's routes, auth, and CORS setup, but runs on inline sample data with a
fixed placeholder price instead of the actual trained pricing model. The full
catalog and model logic are kept in a private repo.

## Structure - Work in Progress

- `web/index.html` — static frontend, no build step
- `api.py` backend: `/api/categories`, `/api/items`, `/api/predict`
