CREATE TABLE IF NOT EXISTS urls (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at DATE
);

ALTER TABLE urls
ALTER COLUMN name TYPE VARCHAR(255);

CREATE TABLE IF NOT EXISTS url_checks (
    id SERIAL PRIMARY KEY,
    url_id INTEGER REFERENCES urls(id),
    status_code INTEGER,
    h1 VARCHAR(255),
    title VARCHAR(255),
    description TEXT,
    created_at DATE
);