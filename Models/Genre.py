from Helpers.constants import PREDEFINED_GENRES, UNKNOWN_GENRE
from db_init import get_db_connection


class Genre:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def get_id_by_name(name):
        """
        Retrieve the ID of a genre by its name.

        Args:
            name (str): The name of the genre to retrieve.

        Returns:
            int or None: The ID of the genre if found, otherwise None.
        """
        with get_db_connection() as conn:
            name = name.lower()
            return conn.execute('SELECT id FROM Genres WHERE name = ?', (name,)).fetchone()['id']

    @staticmethod
    def get_name_by_id(genre_id):
        """
        Retrieve the name of a genre by its ID.

        Args:
            genre_id (int): The ID of the genre to retrieve.

        Returns:
            str or None: The name of the genre if found, otherwise None.
        """
        with get_db_connection() as conn:
            return conn.execute('SELECT name FROM Genres WHERE id = ?', (genre_id,)).fetchone()['name']

    @staticmethod
    def get_all():
        """
        Retrieve all genres from the database.

        Returns:
            list: A list of dictionaries representing all genres, each dictionary containing genre details.
        """
        with get_db_connection() as conn:
            return conn.execute('SELECT * FROM Genres').fetchall()

    @staticmethod
    def get_genre_id_or_default(genre):
        """
        Retrieve the ID of a genre by its name or default to a predefined genre if not found.

        Args:
            genre (str): The name of the genre to retrieve.

        Returns:
            int: The ID of the genre found or the ID of the default genre ('unknown') if not found.
        """
        genre = genre.lower()
        genre_id = Genre.get_id_by_name(genre)

        if genre_id and genre != UNKNOWN_GENRE:
            return genre_id
        else:
            print(
                f"Genre '{genre}' not found in predefined genres. Predefined genres are: {', '.join(PREDEFINED_GENRES)}.")
            print(f"Defaulting to '{UNKNOWN_GENRE}'.")

            genre_id = Genre.get_id_by_name(UNKNOWN_GENRE)
            return genre_id
