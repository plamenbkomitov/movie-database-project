import sqlite3

from db_init import get_db_connection
from Models.Genre import Genre
import datetime


class Movie:
    def __init__(self, id, title, description, release_date, director, genre_id, likes):
        self.id = id
        self.title = title
        self.description = description
        self.release_date = release_date
        self.director = director
        self.genre_id = genre_id
        self.likes = likes

    @staticmethod
    def validate_date(date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return date_text
        except ValueError:
            print("Incorrect date format, try again with the following one: YYYY-MM-DD")
            return None

    @staticmethod
    def add(title, description, release_date, director, genre):
        release_date = Movie.validate_date(release_date)
        if release_date is None:
            return None

        genre_id = Genre.get_genre_id_or_default(genre)
        if genre_id is None:
            return None

        try:
            if Movie.movie_exists(title, release_date, director):
                print("Movie already exists in the database.")
                return None

            with get_db_connection() as conn:
                conn.execute(
                    'INSERT INTO Movies (title, description, release_date, director, genre_id, likes) VALUES (?, ?, '
                    '?, ?,'
                    '?, 0)',
                    (title, description, release_date, director, genre_id)
                )
                movie_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
                return movie_id
        except sqlite3.IntegrityError as e:
            print(f"IntegrityError occurred: {e}")
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def movie_exists(title, release_date, director):
        with get_db_connection() as conn:
            existing_movie = conn.execute(
                'SELECT id FROM Movies WHERE title = ? AND release_date = ? AND director = ?',
                (title, release_date, director)
            ).fetchone()

            return existing_movie is not None

    @staticmethod
    def favourite_movie(movie_id):
        if not Movie.get_by_id(movie_id):
            print(f"Movie with ID {movie_id} does not exist.")
            return
        with get_db_connection() as conn:
            conn.execute('UPDATE Movies SET likes = likes + 1 WHERE id = ?', (movie_id,))

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            return conn.execute('''
                SELECT m.*, g.name as genre_name
                FROM Movies m
                LEFT JOIN Genres g ON m.genre_id = g.id
            ''').fetchall()

    @staticmethod
    def get_by_id(movie_id):
        with get_db_connection() as conn:
            return conn.execute('''
                SELECT m.*, g.name as genre_name
                FROM Movies m
                LEFT JOIN Genres g ON m.genre_id = g.id
                WHERE m.id = ?
            ''', (movie_id,)).fetchone()

    @staticmethod
    def search_by_title(query):
        with get_db_connection() as conn:
            return conn.execute('''
                SELECT m.*, g.name as genre_name
                FROM Movies m
                LEFT JOIN Genres g ON m.genre_id = g.id
                WHERE m.title LIKE ?
            ''', ('%' + query + '%',)).fetchall()

    @staticmethod
    def get_top_liked(limit=5):
        with get_db_connection() as conn:
            return conn.execute('''
                SELECT m.*, g.name as genre_name
                FROM Movies m
                LEFT JOIN Genres g ON m.genre_id = g.id
                ORDER BY m.likes DESC
                LIMIT ?
            ''', (limit,)).fetchall()

    @staticmethod
    def get_newest(limit=5):
        with get_db_connection() as conn:
            return conn.execute('''
                SELECT m.*, g.name as genre_name
                FROM Movies m
                LEFT JOIN Genres g ON m.genre_id = g.id
                ORDER BY date(m.release_date) DESC
                LIMIT ?
            ''', (limit,)).fetchall()

    @staticmethod
    def get_by_genre(genre_name, limit=5):
        with get_db_connection() as conn:
            genre_name = genre_name.lower()
            return conn.execute('''
                SELECT m.*, g.name as genre_name
                FROM Movies m
                LEFT JOIN Genres g ON m.genre_id = g.id
                WHERE g.name = ?
                ORDER BY m.likes DESC
                LIMIT ?
            ''', (genre_name, limit)).fetchall()
