-- references is a reserved word in SQL, so we use reference_values instead
CREATE TABLE IF NOT EXISTS reference_values(
  id SERIAL PRIMARY KEY,
  --citation_key VARCHAR(100) UNIQUE DEFAULT, -- TODO: add citaion key later
  year INT NOT NULL,
  author VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  reftype VARCHAR(50) NOT NULL
)