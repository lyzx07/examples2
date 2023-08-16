-- SQLite
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);
SELECT hash
FROM users;
SELECT hash
FROM users
WHERE username = 'lyzx' ATTACH 'rate-app.db-journal' AS journal;
PRAGMA journal_mode = DELETE;
BEGIN TRANSACTION;
INSERT INTO main.rate - app
SELECT *
FROM journal.rate - app;
COMMIT;
ALTER TABLE users
MODIFY username VARCHAR(255);
ALTER TABLE users
MODIFY COLUMN username VARCHAR(255);
PRAGMA lock_status DROP TABLE songs;
DROP TABLE creator;
ALTER TABLE creators
ADD COLUMN user_id INTEGER REFERENCES users(id);
ALTER TABLE creators
ADD COLUMN channelId TEXT
ALTER TABLE creator
MODIFY COLUMN user_id
SET NOT NULL;
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    channel_id TEXT NOT NULL,
    note TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES creators(channel_id),
    FOREIGN KEY (user_id) REFERENCES creators(user_id)
);

ALTER TABLE users
ADD COLUMN password_bcrypt TEXT;

CREATE TABLE IF NOT EXISTS creators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    description TEXT,
    thumbnail TEXT,
    subscriberCount INTEGER,
    videoCount INTEGER,
    user_id INTEGER NOT NULL,
    channel_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id))

CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rate_value INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        channel_id TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES creators(user_id),
        FOREIGN KEY(channel_id) REFERENCES creators(channel_id))    