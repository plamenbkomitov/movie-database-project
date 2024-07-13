import sqlite3

DB = 'movies.db'


def get_db_connection():
    db_connection = sqlite3.connect(DB)
    db_connection.row_factory = sqlite3.Row
    return db_connection


def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS Movies (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        release_date DATE,
                        director TEXT,
                        genre_id INTEGER,
                        likes INTEGER DEFAULT 0,
                        FOREIGN KEY (genre_id) REFERENCES Genres(id)
                    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS Genres (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()
