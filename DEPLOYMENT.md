# DEPLOYMENT

## FRONTEND — Vercel

Root directory:
`crop disease detection folder/crop-app`

Build:
`npm run build`

Output:
`dist`

Environment:
`VITE_API_BASE_URL=<backend URL>`

## BACKEND

Python version:
3.11

Install:
`pip install -r requirements.txt`

Start:
`gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 180`

Environment variables:

- `FRONTEND_ORIGIN`
- `FASALRAKSHAK_DB_PATH` (optional persistent storage)

**SQLite Persistence Limitation:**
LIVE LOCAL DATA requires persistent backend storage. If deployed without a persistent volume, History and Live Community data may reset after a service restart or redeploy. DEMO DATA does not depend on SQLite persistence and will continue working independently.
