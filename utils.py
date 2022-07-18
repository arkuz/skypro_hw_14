from DAO.netflix_dao import NetflixDAO


def actors_seen_twice(dao: NetflixDAO, actor1: str, actor2: str) -> list[str]:
    """Функция возвращает список актеров, которые играют в паре с actor1 и actor2 больше 2 раз"""
    actors_list = []
    dao_result = dao.get_all_actors_by_actor1_and_actor2(actor1, actor2)
    for row in dao_result:
        actors_list.extend(row['cast'].split(', '))
    return list({actor for actor in actors_list if actors_list.count(actor) > 2})
