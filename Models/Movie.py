import sqlite3

from db_init import get_db_connection
from Models.Genre import Genre
from Helpers.movie_cover import get_movie_cover_from_url
import datetime


class Movie:
    def __init__(self, id, title, description, release_date, director, genre_id, likes, cover):
        self.id = id
        self.title = title
        self.description = description
        self.release_date = release_date
        self.director = director
        self.genre_id = genre_id
        self.likes = likes
        self.cover = cover

    @staticmethod
    def validate_date(date_text):
        """
        Validate the format of the given date string.

        Args:
            date_text (str): The date string to be validated.

        Returns:
            str or None: The validated date string in 'YYYY-MM-DD' format if valid, otherwise None.
        """
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return date_text
        except ValueError:
            print("Incorrect date format, try again with the following one: YYYY-MM-DD")
            return None

    @staticmethod
    def add(title, description, release_date, director, genre):
        """
        Add a new movie to the database.

        Args:
            title (str): The title of the movie.
            description (str): The description or plot summary of the movie.
            release_date (str): The release date of the movie in 'YYYY-MM-DD' format.
            director (str): The director of the movie.
            genre (str): The genre of the movie.

        Returns:
            int or None: The ID of the newly added movie if successful, otherwise None.
        """
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
        """
        Check if a movie already exists in the database based on title, release date, and director.

        Args:
            title (str): The title of the movie.
            release_date (str): The release date of the movie in 'YYYY-MM-DD' format.
            director (str): The director of the movie.

        Returns:
            bool: True if a movie with the given details exists, otherwise False.
        """
        with get_db_connection() as conn:
            existing_movie = conn.execute(
                'SELECT id FROM Movies WHERE title = ? AND release_date = ? AND director = ?',
                (title, release_date, director)
            ).fetchone()

            return existing_movie is not None

    @staticmethod
    def favourite_movie(movie_id):
        """
        Mark a movie as favorite by incrementing its like count.

        Args:
            movie_id (int): The ID of the movie to mark as favorite.
        """
        if not Movie.get_by_id(movie_id):
            print(f"Movie with ID {movie_id} does not exist.")
            return
        with get_db_connection() as conn:
            conn.execute('UPDATE Movies SET likes = likes + 1 WHERE id = ?', (movie_id,))

    @staticmethod
    def get_all():
        """
        Retrieve all movies from the database.

        Returns:
            list: A list of dictionaries representing all movies, each dictionary containing movie details.
        """
        with get_db_connection() as conn:
            return conn.execute('''
                SELECT m.*, g.name as genre_name
                FROM Movies m
                LEFT JOIN Genres g ON m.genre_id = g.id
            ''').fetchall()

    @staticmethod
    def get_by_id(movie_id):
        """
        Retrieve a movie from the database by its ID.

        Args:
            movie_id (int): The ID of the movie to retrieve.

        Returns:
            dict or None: A dictionary containing movie details if found, otherwise None.
        """
        with get_db_connection() as conn:
            return conn.execute('''
                SELECT m.*, g.name as genre_name
                FROM Movies m
                LEFT JOIN Genres g ON m.genre_id = g.id
                WHERE m.id = ?
            ''', (movie_id,)).fetchone()

    @staticmethod
    def search_by_title(query):
        """
        Search movies in the database by title.

        Args:
            query (str): The search query for movie titles.

        Returns:
            list: A list of dictionaries representing movies that match the search query.
        """
        with get_db_connection() as conn:
            return conn.execute('''
                SELECT m.*, g.name as genre_name
                FROM Movies m
                LEFT JOIN Genres g ON m.genre_id = g.id
                WHERE m.title LIKE ?
            ''', ('%' + query + '%',)).fetchall()

    @staticmethod
    def get_top_liked(limit=5):
        """
        Retrieve top movies by likes from the database.

        Args:
            limit (int): Maximum number of movies to retrieve (default is 5).

        Returns:
            list: A list of dictionaries representing top liked movies.
        """
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
        """
        Retrieve newest movies from the database.

        Args:
            limit (int): Maximum number of movies to retrieve (default is 5).

        Returns:
            list: A list of dictionaries representing newest movies.
        """
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
        """
        Retrieve movies by genre from the database.

        Args:
            genre_name (str): The name of the genre to filter movies.
            limit (int): Maximum number of movies to retrieve (default is 5).

        Returns:
            list: A list of dictionaries representing movies of the specified genre.
        """
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

    @staticmethod
    def add_movie_cover_url(movie_id, image_url):
        """
        Add or update the cover image URL of a movie in the database.

        Args:
            movie_id (int): The ID of the movie to update.
            image_url (str): The URL of the cover image to set.

        Returns:
            bool: True if the cover image was successfully updated, otherwise False.
        """
        try:
            with get_db_connection() as conn:
                result = conn.execute('UPDATE Movies SET cover = ? WHERE id = ?', (image_url, movie_id))
                if result.rowcount == 0:
                    return False
                return True
        except sqlite3.IntegrityError as e:
            print(f"IntegrityError occurred: {e}")
            return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False

    @staticmethod
    def get_movie_cover(movie_id):
        """
        View the ASCII art representation of a movie cover.

        Args:
            movie_id (int): The ID of the movie to retrieve the cover image URL from the database.

        Returns:
            str or None: The ASCII art representation of the cover image if found, otherwise None.
        """
        with get_db_connection() as conn:
            result = conn.execute('SELECT cover FROM Movies WHERE id = ?', (movie_id,)).fetchone()
            if result is None:
                print(f"Movie with ID {movie_id} does not exist.")
                return None
            if result['cover']:
                return get_movie_cover_from_url(result['cover'])
            else:
                return None
