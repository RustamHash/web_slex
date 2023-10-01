CREATE TABLE IF NOT EXISTS contracts (
id integer PRIMARY KEY AUTOINCREMENT,
title text UNIQUE NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
login text UNIQUE NOT NULL,
password text NOT NULL,
name text NOT NULL
);