import sqlite3


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SQLiteConnection:
    def __init__(self, filename):
        connection = sqlite3.connect(filename, check_same_thread=False)
        connection.row_factory = _dict_factory
        self.connection = connection

    def __enter__(self):
        return self.connection

    def __exit__(self, *args):
        self.connection.close()


class NetflixDAO:
    cursor = None

    def __init__(self, connection):
        self.cursor = connection.cursor()

    def get_movie_by_title(self, title: str) -> dict:
        """Поиск по названию, если фильмов несколько, выведим самый свежий"""
        query = ("SELECT title, country, release_year, listed_in as genre, description "
                 "FROM netflix "
                 "WHERE title LIKE (?) "
                 "ORDER BY release_year DESC ")
        substring_pattern = f"%{title}%"
        self.cursor.execute(query, (substring_pattern,))
        return self.cursor.fetchone()

    def get_movies_year_to_year(self, year_from: int, year_to: int, limit: int = 100) -> list[dict]:
        """Поиск фильмов поиск по диапазону лет выпуска"""
        query = ("SELECT title, release_year "
                 "FROM netflix "
                 "WHERE release_year BETWEEN (?) AND (?) "
                 "ORDER BY release_year DESC "
                 "LIMIT (?) ")
        self.cursor.execute(query, (year_from, year_to, limit))
        return self.cursor.fetchall()

    def get_movies_by_rating(self, rating: tuple) -> list[dict]:
        """Поиск фильмов по группам рейтинга"""
        questions = ', '.join(['?'] * len(rating))
        query = ("SELECT title, rating, description "
                 "FROM netflix "
                 "WHERE rating in (" + questions + ") ")
        self.cursor.execute(query, rating)
        return self.cursor.fetchall()

    def get_movies_by_genre(self, genre: str, limit: int = 10) -> list[dict]:
        """Поиск фильмов поиск по жанру"""
        query = ("SELECT title, description "
                 "FROM netflix "
                 "WHERE listed_in LIKE (?) "
                 "ORDER BY release_year DESC "
                 "LIMIT ? ")
        substring_pattern = f"%{genre}%"
        self.cursor.execute(query, (substring_pattern, limit))
        return self.cursor.fetchall()

    def get_all_actors_by_actor1_and_actor2(self, actor1: str, actor2: str) -> list[dict]:
        """Получить все записи с актерами, где встречаются actor1 и actor2"""
        query = ("SELECT netflix.cast "
                 "FROM netflix "
                 "WHERE netflix.cast LIKE (?) "
                 "AND netflix.cast LIKE (?) ")
        actor1_pattern = f"%{actor1}%"
        actor2_pattern = f"%{actor2}%"
        self.cursor.execute(query, (actor1_pattern, actor2_pattern))
        return self.cursor.fetchall()

    def get_video_by_filter(self, type: str, genre: str, release_year: int) -> list[dict]:
        """Поиск картин по типу, жанру, году выпуска"""
        query = ("SELECT * "
                 "FROM netflix "
                 "WHERE type = (?) "
                 "AND listed_in LIKE (?) "
                 "AND release_year = (?) ")
        genre_pattern = f"%{genre}%"
        self.cursor.execute(query, (type, genre_pattern, release_year))
        return self.cursor.fetchall()
