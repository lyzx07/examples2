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
DROP TABLE highlight_notes;
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
    note TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES creators(channel_id),
    FOREIGN KEY (user_id) REFERENCES creators(user_id)
);
CREATE TABLE subscribed (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    channel_id TEXT NOT NULL,
    subscribed BOOLEAN NOT NULL,
    FOREIGN KEY (channel_id) REFERENCES creators(channel_id),
    FOREIGN KEY (user_id) REFERENCES creators(user_id)
);
CREATE TABLE IF NOT EXISTS highlight_notes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    channel_id TEXT NOT NULL,
    highlighted_note TEXT,
    FOREIGN KEY (channel_id) REFERENCES creators(channel_id),
    FOREIGN KEY (user_id) REFERENCES creators(user_id)
);

created_at TEXT NOT NULL DEFAULT (
        strftime('%d/%m/%Y %H:%M:%S', 'now', 'localtime')
    ),
    
CREATE TABLE IF NOT EXISTS watched (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    video_id TEXT NOT NULL,
    title TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (strftime('%d/%m/%Y', 'now', 'localtime')),
    FOREIGN KEY (video_id) REFERENCES tunes(video_id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
CREATE TABLE IF NOT EXISTS tunes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    video_id TEXT NOT NULL,
)
ALTER TABLE notes
ADD COLUMN highlighted_note TEXT;
CREATE TABLE IF NOT EXISTS creators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    description TEXT,
    thumbnail TEXT,
    subscriberCount INTEGER,
    videoCount INTEGER,
    user_id INTEGER NOT NULL,
    channel_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
) CREATE TABLE IF NOT EXISTS ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rate_value INTEGER NOT NULL,
    likeability INTEGER,
    humor INTEGER,
    pity_subscription INTEGER,
    informative INTEGER,
    silly INTEGER,
    funny INTEGER,
    serious INTEGER,
    deadpan INTEGER,
    lets_be_friends INTEGER,
    genuine INTEGER,
    fake INTEGER,
    relatable INTEGER,
    emotional INTEGER,
    inspirational INTEGER,
    controversial INTEGER,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    channel_id TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES creators(user_id),
    FOREIGN KEY(channel_id) REFERENCES creators(channel_id)
)