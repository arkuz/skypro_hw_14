import sqlite3

import const


class DB:
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.connection.row_factory = self.__dict_factory

    @staticmethod
    def __dict_factory(cursor: sqlite3.Cursor, row: tuple) -> dict:
        return {
            col[0]: row[idx]
            for idx, col in enumerate(cursor.description)
        }

    def __enter__(self) -> sqlite3.Cursor:
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, *args):
        self.cursor.close()
        self.connection.close()


class NetflixDAO:

    def get_movie_by_title(self, title: str) -> dict:
        """Поиск по названию, если фильмов несколько, выведим самый свежий"""
        with DB(const.DB.FILENAME) as cursor:
            query = ("SELECT title, country, release_year, listed_in as genre, description "
                     "FROM netflix "
                     "WHERE title LIKE (?) "
                     "ORDER BY release_year DESC ")
            substring_pattern = f"%{title}%"
            cursor.execute(query, (substring_pattern,))
            return cursor.fetchone()

    def get_movies_year_to_year(self, year_from: int, year_to: int, limit: int = 100) -> list[dict]:
        """Поиск фильмов поиск по диапазону лет выпуска"""
        with DB(const.DB.FILENAME) as cursor:
            query = ("SELECT title, release_year "
                     "FROM netflix "
                     "WHERE release_year BETWEEN (?) AND (?) "
                     "ORDER BY release_year DESC "
                     "LIMIT (?) ")
            cursor.execute(query, (year_from, year_to, limit))
            return cursor.fetchall()

    def get_movies_by_rating(self, rating: tuple) -> list[dict]:
        """Поиск фильмов по группам рейтинга"""
        with DB(const.DB.FILENAME) as cursor:
            questions = ', '.join(['?'] * len(rating))
            query = ("SELECT title, rating, description "
                     "FROM netflix "
                     "WHERE rating in (" + questions + ") ")
            cursor.execute(query, rating)
            return cursor.fetchall()

    def get_movies_by_genre(self, genre: str, limit: int = 10) -> list[dict]:
        """Поиск фильмов поиск по жанру"""
        with DB(const.DB.FILENAME) as cursor:
            query = ("SELECT title, description "
                     "FROM netflix "
                     "WHERE listed_in LIKE (?) "
                     "ORDER BY release_year DESC "
                     "LIMIT ? ")
            substring_pattern = f"%{genre}%"
            cursor.execute(query, (substring_pattern, limit))
            return cursor.fetchall()

    def get_all_actors_by_actor1_and_actor2(self, actor1: str, actor2: str) -> list[dict]:
        """Получить все записи с актерами, где встречаются actor1 и actor2"""
        with DB(const.DB.FILENAME) as cursor:
            query = ("SELECT netflix.cast "
                     "FROM netflix "
                     "WHERE netflix.cast LIKE (?) "
                     "AND netflix.cast LIKE (?) ")
            actor1_pattern = f"%{actor1}%"
            actor2_pattern = f"%{actor2}%"
            cursor.execute(query, (actor1_pattern, actor2_pattern))
            return cursor.fetchall()

    def get_video_by_filter(self, type: str, genre: str, release_year: int) -> list[dict]:
        """Поиск картин по типу, жанру, году выпуска"""
        with DB(const.DB.FILENAME) as cursor:
            query = ("SELECT * "
                     "FROM netflix "
                     "WHERE type = (?) "
                     "AND listed_in LIKE (?) "
                     "AND release_year = (?) ")
            genre_pattern = f"%{genre}%"
            cursor.execute(query, (type, genre_pattern, release_year))
            return cursor.fetchall()
