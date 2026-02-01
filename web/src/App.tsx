import { useState } from "react";
import { getOfficer, Officer, OfficerDetail, searchOfficers } from "./api";

export default function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Officer[]>([]);
  const [selected, setSelected] = useState<OfficerDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const runSearch = async () => {
    setError(null);
    setSelected(null);
    if (query.trim().length < 2) {
      setError("Please enter at least 2 characters.");
      return;
    }
    try {
      setLoading(true);
      const data = await searchOfficers(query.trim());
      setResults(data);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const loadOfficer = async (id: number) => {
    setError(null);
    try {
      setLoading(true);
      const data = await getOfficer(id);
      setSelected(data);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>IAS Officer Directory</h1>
        <p>Search officers and view posting history.</p>
      </header>

      <section className="search">
        <input
          type="text"
          placeholder="Search by officer name"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
        <button onClick={runSearch} disabled={loading}>
          Search
        </button>
      </section>

      {error && <div className="error">{error}</div>}

      <section className="results">
        <h2>Results</h2>
        {results.length === 0 && <p>No results yet.</p>}
        <ul>
          {results.map((officer) => (
            <li key={officer.id}>
              <button className="link" onClick={() => loadOfficer(officer.id)}>
                {officer.full_name}
              </button>
              {officer.batch && <span> | Batch {officer.batch}</span>}
              {officer.cadre && <span> | {officer.cadre}</span>}
              {officer.current_posting && <div>{officer.current_posting}</div>}
            </li>
          ))}
        </ul>
      </section>

      {selected && (
        <section className="profile">
          <h2>Profile</h2>
          <div className="profile-card">
            <h3>{selected.full_name}</h3>
            <p>
              {selected.batch && <span>Batch {selected.batch} </span>}
              {selected.cadre && <span>| {selected.cadre} </span>}
            </p>
            {selected.education && <p>Education: {selected.education}</p>}
            {selected.current_posting && <p>Current: {selected.current_posting}</p>}
            {selected.source_url && (
              <p>
                Source:{" "}
                <a href={selected.source_url} target="_blank" rel="noreferrer">
                  {selected.source_url}
                </a>
              </p>
            )}
          </div>

          <div className="timeline">
            <h3>Posting History</h3>
            {selected.postings.length === 0 && <p>No postings recorded yet.</p>}
            <ul>
              {selected.postings.map((posting) => (
                <li key={posting.id}>
                  <strong>{posting.organization || "Unknown organization"}</strong>
                  {posting.role_title && <span> — {posting.role_title}</span>}
                  {posting.location && <span> ({posting.location})</span>}
                  <div>
                    {posting.start_date && <span>{posting.start_date}</span>}
                    {posting.end_date && <span> → {posting.end_date}</span>}
                    {!posting.end_date && posting.is_current && <span> (current)</span>}
                  </div>
                  {posting.source_url && (
                    <a href={posting.source_url} target="_blank" rel="noreferrer">
                      Source link
                    </a>
                  )}
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}
    </div>
  );
}
