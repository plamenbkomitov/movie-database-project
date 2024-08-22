import sqlite3
from Helpers.constants import DB_NAME, PREDEFINED_GENRES


def get_db_connection():
    db_connection = sqlite3.connect(DB_NAME)
    db_connection.row_factory = sqlite3.Row
    return db_connection


def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS Movies (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL CHECK(LENGTH(title) <= 100),
                        description TEXT NOT NULL CHECK(LENGTH(description) <= 500),
                        release_date DATE NOT NULL,
                        director TEXT NOT NULL CHECK(LENGTH(director) <= 50),
                        genre_id INTEGER NOT NULL,
                        likes INTEGER DEFAULT 0,
                        cover TEXT CHECK(LENGTH(cover) <= 500),
                        FOREIGN KEY (genre_id) REFERENCES Genres(id)
                    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS Genres (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE CHECK(LENGTH(name) <= 50)
                    )''')

    for genre in PREDEFINED_GENRES:
        lowercase_genre = genre.lower()
        conn.execute('INSERT OR IGNORE INTO Genres (name) VALUES (?)', (lowercase_genre,))

    conn.commit()
    conn.close()
