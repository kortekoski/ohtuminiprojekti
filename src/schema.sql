CREATE TABLE todos (
  id SERIAL PRIMARY KEY, 
  content TEXT NOT NULL,
  done BOOLEAN DEFAULT FALSE
);

-- references is a reserved word in SQL, so we use reference_values instead
CREATE TABLE reference_values(
  id SERIAL PRIMARY KEY,
  year INT NOT NULL,
  author VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL
)