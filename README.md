# IAS & Civil Services Officer Directory

Web app that crawls official sources for IAS and other civil services officers,
stores longitudinal posting history, and provides fast search with profile views.

## Structure
- `crawler/`: ingestion pipeline and source parsers
- `api/`: FastAPI service for search and profiles
- `web/`: React UI
- `infra/`: AWS deployment notes and templates

## Quick start (local)
1. Create a Postgres database and set `DATABASE_URL`.
2. Run migrations: `psql "$DATABASE_URL" -f db/migrations/001_init.sql`
3. Crawl: `python crawler/main.py`
4. API: `uvicorn api.app.main:app --reload`
5. Web: `npm install && npm run dev` (from `web/`)

## Quick start (Docker)
1. Run: `docker compose up --build`
2. Open `http://localhost:5173`
3. Use the seeded "Sample Officer" to verify the UI.

## Environment
Copy `.env.example` to `.env` and fill in values.

## Additional sources
Add state cadre sources via `STATE_SOURCE_URLS` (comma-separated).
The crawler will ingest each source and store posting history when available.
Add DoPT PDF sources via `DOPT_PDF_URLS` (comma-separated).

## AWS (serverless)
See `infra/README.md` and `infra/sam/template.yaml` for a starter SAM stack with:
- API Lambda + API Gateway
- Crawler Lambda + monthly EventBridge schedule
