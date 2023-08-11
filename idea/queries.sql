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

ALTER TABLE users MODIFY username VARCHAR(255);

ALTER TABLE users
MODIFY COLUMN username VARCHAR(255);

PRAGMA lock_status

DROP TABLE songs;

DROP TABLE creator;

ALTER TABLE creators ADD COLUMN user_id INTEGER REFERENCES users(id);

ALTER TABLE creators ADD COLUMN channelId TEXT

ALTER TABLE creator
MODIFY COLUMN user_id
SET NOT NULL;