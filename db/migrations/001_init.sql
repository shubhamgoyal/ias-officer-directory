CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE IF NOT EXISTS officers (
  id BIGSERIAL PRIMARY KEY,
  full_name TEXT NOT NULL,
  batch INTEGER,
  cadre TEXT,
  current_posting TEXT,
  education TEXT,
  source_url TEXT,
  last_updated TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (full_name, batch, cadre)
);

CREATE INDEX IF NOT EXISTS idx_officers_name_trgm
  ON officers USING GIN (full_name gin_trgm_ops);

CREATE TABLE IF NOT EXISTS postings (
  id BIGSERIAL PRIMARY KEY,
  officer_id BIGINT NOT NULL REFERENCES officers(id) ON DELETE CASCADE,
  organization TEXT,
  role_title TEXT,
  location TEXT,
  start_date DATE,
  end_date DATE,
  is_current BOOLEAN NOT NULL DEFAULT TRUE,
  source_url TEXT,
  observed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_postings_officer_id ON postings(officer_id);
CREATE INDEX IF NOT EXISTS idx_postings_current ON postings(officer_id, is_current);

CREATE TABLE IF NOT EXISTS source_ingests (
  id BIGSERIAL PRIMARY KEY,
  source_url TEXT NOT NULL,
  source_type TEXT NOT NULL,
  crawled_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  payload_hash TEXT
);
