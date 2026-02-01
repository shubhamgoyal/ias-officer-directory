INSERT INTO officers (full_name, batch, cadre, current_posting, education, source_url)
VALUES
  ('Sample Officer', 2005, 'AGMU', 'Joint Secretary, Sample Dept', 'B.Tech, MPA', 'https://iascivillist.dopt.gov.in/Home/ViewList');

INSERT INTO postings (officer_id, organization, role_title, location, start_date, end_date, is_current, source_url)
VALUES
  (1, 'District Administration', 'District Magistrate', 'Sample City', '2012-06-01', '2015-05-31', false, 'https://example.com'),
  (1, 'State Secretariat', 'Deputy Secretary', 'Sample State', '2015-06-01', '2019-04-30', false, 'https://example.com'),
  (1, 'Sample Dept', 'Joint Secretary', 'New Delhi', '2019-05-01', NULL, true, 'https://example.com');
