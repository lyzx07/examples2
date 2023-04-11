-- SQLite
CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
username TEXT NOT NULL,
hash TEXT NOT NULL);

SELECT hash FROM users;


SELECT hash FROM users WHERE username = 'lyzx'