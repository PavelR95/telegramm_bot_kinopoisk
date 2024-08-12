from core import KinoApi
from utils import formed_data
import datetime

genres_list = ['биография', 'боевик', 'вестерн', 'военный', 'детектив', 'детский', 'для взрослых',
               'документальный', 'драма', 'игра', 'история', 'комедия', 'концерт',
               'криминал', 'мелодрама', 'музыка', 'мюзикл', 'новости', 'приключения', 'реальное ТВ',
               'семейный', 'спорт', 'ток-шоу', 'триллер', 'ужасы', 'фантастика', 'фильм-нуар', 'фэнтези', 'церемония']

api = KinoApi()


def low():
    """
    Отправляет запрос на получение информации о фильмах с премьерой на ближайшие 7 дней от текущей даты.
    :return: Возвращает список фильмов с информацией.
    """
    date_now = datetime.datetime.today()
    date_later = date_now + datetime.timedelta(days=7)
    date_find = '{}-{}'.format(datetime.datetime.strftime(date_now, '%d.%m.%Y'),
                               datetime.datetime.strftime(date_later, '%d.%m.%Y'))
    params = {
        'sortField': 'premiere.russia',
        'sortType': '1',
        'type': 'movie',
        'premiere.russia': '{}'.format(date_find),
        'notNullFields': 'poster.url',
        'limit': '100',
    }
    try:
        data = api.get_answer(params=params, url=api.url_movie)
    except ConnectionError as er:
        return [er]
    return formed_data.form_films_data_list(data)


def high():
    """
    Отправляет запрос на получение информации о топ 10 фильмах.
    :return: Возвращает список фильмов с информацией.
    """
    params = {
        'sortField': 'rating.kp',
        'sortType': '-1',
        'type': 'movie',
        'notNullFields': ['poster.url', 'top250'],
        'limit': '10',
    }
    try:
        data = api.get_answer(params=params, url=api.url_movie)
    except ConnectionError as er:
        return [er]
    return formed_data.form_films_data_list(data)


def custom(genre: list or str = None, year: str = None, limit: int = 10):
    """
    Отправляет запрос на получение информации о фильмах, по указанным параметрам.
    :return: Возвращает список фильмов с информацией.
    """
    params = {
        'sortField': 'rating.kp',
        'sortType': '-1',
        'type': 'movie',
        'notNullFields': 'poster.url',
        'limit': '{}'.format(limit),
    }
    if genre is not None:
        params['genres.name'] = genre
    if year is not None:
        params['year'] = year
    try:
        data = api.get_answer(params=params, url=api.url_movie)
    except ConnectionError as er:
        return [er]
    return formed_data.form_films_data_list(data)


def main():
    print('low премьёры в ближайшие 7 дней\n'
          'high топ 10 фильмов по рейтингу кинопоиска за всё время\n'
          'custom топ фильмов с настройками:\n'
          'exit выход\n')
    while True:
        try:
            films = []
            com = input('Введите команду: ')
            if com == 'exit':
                break
            elif com == 'low':
                films = low()
            elif com == 'high':
                films = high()
            elif com == 'custom':
                print('Выберете жанр. Можно оставить пустым.')
                for id_genre, genre in enumerate(genres_list):
                    if id_genre % 5 == 0:
                        print()
                    print(genre, end=', ')
                print()
                genre = input('Жанр: ')
                if genre == '':
                    genre = None
                print('Введите год или период от 1874 до 2050. Можно оставить пустым.\nНапример: 2017, 1960-2000')
                year = input('Год: ')
                if year == '':
                    year = None
                print('Сколько фильмов показать? Можно оставить пустым. По умолчанию 10')
                limit = input('Лимит: ')
                if limit == '':
                    limit = 10
                films = custom(genre=genre, year=year, limit=limit)
            else:
                print('Вы ввели не верную команду')
            print('\n', '-' * 20, '\n')
            for film in films:
                print(film)
                print('-' * 20)
        except ConnectionError as er:
            print('Возникла ошибка: ', er)


if __name__ == '__main__':
    main()
