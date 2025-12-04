-- -*- mode: sql; sql-product: postgres; -*-
-- references is a reserved word in SQL, so we use reference_values instead
CREATE TABLE IF NOT EXISTS reference_values(
  id SERIAL PRIMARY KEY,
  citation_key VARCHAR(100) UNIQUE,
  year INT NOT NULL,
  title VARCHAR(255) NOT NULL,
  reftype VARCHAR(50) NOT NULL,
  extra JSONB DEFAULT '{}'::jsonb -- the rest of the fields can go here
);

-- Authors table for storing unique author names
CREATE TABLE IF NOT EXISTS authors(
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL
);

-- Many-to-many mapping between references and authors
CREATE TABLE IF NOT EXISTS reference_authors(
  reference_id INT NOT NULL,
  author_id INT NOT NULL,
  author_order INT NOT NULL, -- to preserve the order of authors
  PRIMARY KEY (reference_id, author_id),
  FOREIGN KEY (reference_id) REFERENCES reference_values(id) ON DELETE CASCADE,
  FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
);

-- View that joins references with their authors
CREATE OR REPLACE VIEW references_view AS
SELECT 
  rv.id,
  rv.citation_key,
  rv.year,
  STRING_AGG(a.name, ' and ' ORDER BY ra.author_order) as author,
  rv.title,
  rv.reftype,
  rv.extra
FROM reference_values rv
LEFT JOIN reference_authors ra ON rv.id = ra.reference_id
LEFT JOIN authors a ON ra.author_id = a.id
GROUP BY rv.id, rv.citation_key, rv.year, rv.title, rv.reftype, rv.extra;
