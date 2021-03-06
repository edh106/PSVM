#!/usr/bin/env python

import sqlite3
import hashlib

conn = sqlite3.connect('database.db')
c = conn.cursor()

#Recreate tables from scratch
c.executescript('''

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS code_samples;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS threads;
DROP TABLE IF EXISTS messages;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY, 
    username TEXT NOT NULL COLLATE NOCASE, 
    pass_hash TEXT NOT NULL,
    email TEXT NOT NULL,
    admin INTEGER NOT NULL DEFAULT 0,
    verified INTEGER NOT NULL DEFAULT 0,
    timestamp DATETIME DEFAULT (datetime('now','localtime'))
);

CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE threads (
    thread_id INTEGER PRIMARY KEY,
    category_id INTEGER,
    title TEXT NOT NULL,
    op_id INTEGER,
    timestamp DATETIME DEFAULT (datetime('now','localtime')),
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (op_id) REFERENCES users(user_id)
);
    

CREATE TABLE comments (
    comment_id INTEGER PRIMARY KEY,
    thread_id INTEGER,
    user_id INTEGER NOT NULL,
    body TEXT,
    raw TEXT,
    timestamp DATETIME DEFAULT (datetime('now','localtime')),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (thread_id) REFERENCES threads(thread_id)
);

CREATE TABLE code_samples (
    sample_id INTEGER PRIMARY KEY,
    language TEXT NOT NULL,
    raw TEXT,
    body TEXT
);

CREATE TABLE messages (
    message_id INTEGER PRIMARY KEY,
    body TEXT,
    from_id INTEGER,
    to_id INTEGER,
    timestamp DATETIME DEFAULT (datetime('now','localtime')),
    FOREIGN KEY (from_id) REFERENCES users(user_id),
    FOREIGN KEY (to_id) REFERENCES users(user_id)
);

    ''')

#Add some default values
c.executescript("""

INSERT INTO categories VALUES( NULL, 'C++');
INSERT INTO categories VALUES( NULL, 'Python');
INSERT INTO categories VALUES( NULL, 'General');

""")


user = ('user', hashlib.sha512("password").hexdigest(), "invalid@gmail.com", True, True)
c.execute('''

INSERT INTO users(user_id, username, pass_hash, email, admin, verified)
VALUES(NULL, ?, ?, ?, ?, ?)

''', user)


# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
