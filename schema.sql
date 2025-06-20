-- schema.sql
DROP TABLE IF EXISTS events;

CREATE TABLE events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    description TEXT,
    category    TEXT CHECK(category IN ('Hackathon','Conference','Meetup')) NOT NULL,
    date        TEXT NOT NULL,     -- YYYY-MM-DD
    latitude    REAL NOT NULL,
    longitude   REAL NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
