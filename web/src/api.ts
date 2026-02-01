export interface Officer {
  id: number;
  full_name: string;
  batch?: number | null;
  cadre?: string | null;
  current_posting?: string | null;
  education?: string | null;
  source_url?: string | null;
  last_updated: string;
}

export interface Posting {
  id: number;
  officer_id: number;
  organization?: string | null;
  role_title?: string | null;
  location?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  is_current: boolean;
  source_url?: string | null;
  observed_at: string;
}

export interface OfficerDetail extends Officer {
  postings: Posting[];
}

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function searchOfficers(query: string): Promise<Officer[]> {
  const resp = await fetch(`${API_BASE}/officers?name=${encodeURIComponent(query)}`);
  if (!resp.ok) {
    throw new Error("Failed to search officers");
  }
  return resp.json();
}

export async function getOfficer(id: number): Promise<OfficerDetail> {
  const resp = await fetch(`${API_BASE}/officers/${id}`);
  if (!resp.ok) {
    throw new Error("Failed to load officer profile");
  }
  return resp.json();
}
