import logging
from DAO.netflix_dao import NetflixDAO
from const import ErrorCode, RatingGroup
from flask import Blueprint, jsonify

logger = logging.getLogger(__name__)

netflix_blueprint = Blueprint('netflix_blueprint', __name__, template_folder='templates')

netflix_dao = NetflixDAO('netflix.db')


@netflix_blueprint.route('/movie/<title>/')
def movie_by_title_page(title):
    logger.info(f'Обращение к "/movie/{title}/"')
    movie = netflix_dao.get_movie_by_title(title)
    return jsonify(movie)


@netflix_blueprint.route('/movie/<int:year_from>/to/<int:year_to>/')
def movies_year_to_year_page(year_from, year_to):
    logger.info(f'Обращение к "/movie/{year_from}/to/{year_to}/"')
    movies = netflix_dao.get_movies_year_to_year(year_from, year_to)
    return jsonify(movies)


@netflix_blueprint.route('/rating/<group>/')
def movies_by_rating_page(group):
    logger.info(f'Обращение к "/rating/{group}/"')
    groups = {
        'children': RatingGroup.CHILDREN,
        'family': RatingGroup.FAMILY,
        'adult': RatingGroup.ADULT,
    }
    current_group = groups.get(group)
    if not current_group:
        logger.error(ErrorCode.ERROR_404)
        return jsonify(ErrorCode.ERROR_404)

    movies = netflix_dao.get_movies_by_rating(current_group)
    return jsonify(movies)


@netflix_blueprint.route('/genre/<genre>/')
def movies_by_genre_page(genre):
    logger.info(f'Обращение к "/genre/<genre>/"')
    movies = netflix_dao.get_movies_by_genre(genre)
    return jsonify(movies)


@netflix_blueprint.errorhandler(ErrorCode.ERROR_404['code'])
def error_page_404(e):
    logger.error(ErrorCode.ERROR_404)
    return jsonify(ErrorCode.ERROR_404)


@netflix_blueprint.errorhandler(ErrorCode.ERROR_500['code'])
def error_page_500(e):
    logger.error(ErrorCode.ERROR_500)
    return jsonify(ErrorCode.ERROR_500)
