-- SQLite
CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
username TEXT NOT NULL,
hash TEXT NOT NULL);

SELECT hash FROM users;


SELECT hash FROM users WHERE username = 'lyzx'

ATTACH 'rate-app.db-journal' AS journal;
PRAGMA journal_mode = DELETE;
BEGIN TRANSACTION;
INSERT INTO main.rate-app SELECT * FROM journal.rate-app;
COMMIT;