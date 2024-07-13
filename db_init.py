import sqlite3

DB = 'movies.db'


def get_db_connection():
    db_connection = sqlite3.connect(DB)
    db_connection.row_factory = sqlite3.Row
    return db_connection


def init_db():
    get_db_connection().execute('''CREATE TABLE IF NOT EXISTS Movies (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            description TEXT,
                            release_date DATE,
                            director TEXT,
                            user_rating INTEGER DEFAULT 0
                        )''')
    get_db_connection().execute('''CREATE TABLE IF NOT EXISTS Genres (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL
                        )''')
    get_db_connection().execute('''CREATE TABLE IF NOT EXISTS MovieGenres (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            movie_id INTEGER,
                            genre_id INTEGER,
                            FOREIGN KEY (movie_id) REFERENCES Movies(id),
                            FOREIGN KEY (genre_id) REFERENCES Genres(id)
                        )''')
