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

## Environment
Copy `.env.example` to `.env` and fill in values.
