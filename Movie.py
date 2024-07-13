from db_init import get_db_connection
from Genre import Genre


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
    def add(title, description, release_date, director, genre):
        genre_info = Genre.get_by_name(genre)

        if genre_info:
            genre_id = genre_info['id']
        else:
            genre_id = Genre.add(genre)
        with get_db_connection() as conn:
            conn.execute(
                'INSERT INTO Movies (title, description, release_date, director, genre_id, likes) VALUES (?, ?, '
                '?, ?, ?, ?)',
                (title, description, release_date, director, genre_id, 0)
            )

    @staticmethod
    def favourite_movie(movie_id):
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
                ORDER BY m.release_date DESC
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
