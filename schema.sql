DROP TABLE IF EXISTS rsvp;
CREATE TABLE rsvp (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  availability TEXT,
  guests INTEGER,
  poll TEXT,
  timestamp INTEGER
);
