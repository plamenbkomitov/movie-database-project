from db_init import get_db_connection


class Genre:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def add(name):
        with get_db_connection() as conn:
            name = name.lower()
            conn.execute('INSERT INTO Genres (name) VALUES (?)', (name,))
            return conn.execute('SELECT id FROM Genres WHERE name = ?', (name,)).fetchone()['id']

    @staticmethod
    def get_by_name(name):
        with get_db_connection() as conn:
            name = name.lower()
            return conn.execute('SELECT id FROM Genres WHERE name = ?', (name,)).fetchone()

    @staticmethod
    def get_name_by_id(genre_id):
        with get_db_connection() as conn:
            return conn.execute('SELECT name FROM Genres WHERE id = ?', (genre_id,)).fetchone()['name']

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            return conn.execute('SELECT * FROM Genres').fetchall()
