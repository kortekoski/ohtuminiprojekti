-- references is a reserved word in SQL, so we use reference_values instead
CREATE TABLE reference_values(
  id SERIAL PRIMARY KEY,
  year INT NOT NULL,
  author VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  type VARCHAR(50) NOT NULL
)