class Rating:
    """Возрастные ограничения"""
    G = 'G'
    PG = 'PG'
    PG_13 = 'PG-13'
    R = 'R'
    NC_17 = 'NC-17'


class RatingGroup:
    """Группы возрастных ограничений"""
    CHILDREN = (Rating.G,)
    FAMILY = (Rating.G, Rating.PG, Rating.PG_13)
    ADULT = (Rating.R, Rating.NC_17)


class ErrorCode:
    """Коды ошибок"""
    ERROR_404 = {'code': 404, 'text': 'Page not found'}
    ERROR_500 = {'code': 500, 'text': 'Internal Server Error'}

class ErrorMessage:
    """Пользовательские сообщения об ошибках"""
    EMPTY_RESULT = {'type': 'error', 'message': 'Empty result'}

class DB:
    FILENAME = 'netflix.db'

