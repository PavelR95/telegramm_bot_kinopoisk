import datetime

from telebot.types import Message
from kinopoisk_api.core import KinoApi
from kinopoisk_api.utils import formed_data

from database.utils.database_manager import DatabaseManager
from database.utils.history_manager import DatabaseHistoryManager
from database.common.models import Users, CustomsStatus

from logging_manager.core import LoggerManager

kinopoisk_api = KinoApi()
database_manager = DatabaseManager

genres_list = ['биография', 'боевик', 'вестерн', 'военный', 'детектив', 'детский', 'для взрослых',
               'документальный', 'драма', 'игра', 'история', 'комедия', 'концерт',
               'криминал', 'мелодрама', 'музыка', 'мюзикл', 'новости', 'приключения', 'реальное ТВ',
               'семейный', 'спорт', 'ток-шоу', 'триллер', 'ужасы', 'фантастика', 'фильм-нуар', 'фэнтези', 'церемония']

help_message = [
    'Доступные команды:\n'
    '/low - Все премьеры в ближайшие 7 дней.\n'
    '/high - Топ 10 фильмов за всё время по версии кинопоиска\n'
    '/custom - Топ фильмов с параметрами поиска\n'
    '/history - Просмотреть последние 3 запроса\n'
    '/help - Просмотр текущих команд\n'
]


def cmd_start_hello(message: Message, user: Users) -> list:
    text_answer = (
        "Привета! Моя джа джа... Прошу прощения это из другой реплики."
        "\nПривет я бот, который помогает в поиске кино на вечер.."
    )
    return [text_answer]


def cmd_help(message: Message, user: Users) -> list:
    LoggerManager.logging(user=user, message=message, command='/help')
    DatabaseHistoryManager.set_history_user(user=user, data_history='/help')
    return help_message


def cmd_low(message: Message, user: Users) -> list:
    """
    Отправляет запрос на получение информации о фильмах с премьерой на ближайшие 7 дней от текущей даты.
    :return: Возвращает список сообщений которые нужно отправить пользователю.
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
        data = kinopoisk_api.get_answer(params, kinopoisk_api.url_movie)
    except ConnectionError as er:
        LoggerManager.logging(user=user, message=message, command='/low {}'.format(er))
        return [er] + cmd_help(message=message, user=user)
    LoggerManager.logging(user=user, message=message, command='/low')
    DatabaseHistoryManager.set_history_user(user=user, data_history='/low')
    return formed_data.form_films_data_list(data) + help_message


def cmd_high(message: Message, user: Users) -> list:
    """
    Отправляет запрос на получение информации о топ 10 фильмах.
    :return: Возвращает список строк, которые необходимо отправить.
    """
    params = {
        'sortField': 'rating.kp',
        'sortType': '-1',
        'type': 'movie',
        'notNullFields': ['poster.url', 'top250'],
        'limit': '10',
    }
    try:
        data = kinopoisk_api.get_answer(params=params, url=kinopoisk_api.url_movie)
    except ConnectionError as er:
        LoggerManager.logging(user=user, message=message, command='/high {}'.format(er))
        return [er] + cmd_help(message=message, user=user)
    LoggerManager.logging(user=user, message=message, command='/high')
    DatabaseHistoryManager.set_history_user(user=user, data_history='/high')
    return formed_data.form_films_data_list(data) + help_message


def cmd_custom_genres(message: Message, user: Users, status_user: CustomsStatus) -> list or None:
    """
    Функция изменяет переменную genre в CustomsStatus пользователя. И проверяет его в доступных жанрах
    Если ни один жанр не был найден вернёт сообщение ошибки. Возвращает сообщение с инструкциями или None
    """
    if not status_user.status_genres:
        database_manager.set_status_genres(status_user, True)
        return [
            'Доступный список жанров: {genres}\n\n'
            'Введите интересующие вас жанры через пробел или запятую\n'
            'Например: вестерн, комедия\n\n'
            '/clear - отчистка фильтра\n'
            '/return - вернутся назад\n'.format(
                genres=', '.join(genres_list)
            )
        ]
    if message.text == '/clear':
        database_manager.set_genres(status_user=status_user, genres=DatabaseManager.default_genres)
        database_manager.set_status_genres(status_user=status_user, status=False)
        return None
    if message.text == '/return':
        database_manager.set_status_genres(status_user=status_user, status=False)
        return None
    genres = message.text.lower().split()
    genres = [genre.strip(',') for genre in genres if genre.strip(',') in genres_list]
    if not genres:
        database_manager.set_status_genres(status_user=status_user, status=False)
        raise ValueError('Не удалось добавить жанры')
    database_manager.set_genres(status_user=status_user, genres=', '.join(genres))
    database_manager.set_status_genres(status_user, False)
    return None


def cmd_custom_years(message: Message, user: Users, status_user: CustomsStatus) -> list or None:
    """
    Функция изменяет переменную years в CustomsStatus пользователя, и проверяет её.
    Если проверка не успешна вернёт ошибку
    """
    if not status_user.status_years:
        database_manager.set_status_years(status_user, True)
        return [
            'Введите год или период от 1874 до 2050. Можно оставить пустым.\n'
            'Например: 2017, 1960-2000\n\n'
            '/clear - отчистка фильтра\n'
            '/return - вернутся назад\n'
        ]
    if message.text == '/clear':
        database_manager.set_years(status_user=status_user, years=DatabaseManager.default_years)
        database_manager.set_status_years(status_user=status_user, status=False)
        return None
    if message.text == '/return':
        database_manager.set_status_years(status_user=status_user, status=False)
        return None
    years = message.text.lower().strip(' ').strip(',').split('-')
    years = [year.strip(' ').strip(',') for year in years]
    try:
        for year in years:
            try:
                year_number = int(year)
            except ValueError:
                raise ValueError('Не правильно указан год')
            print(2050 < year_number < 1874)
            if 2050 < year_number or year_number < 1874:
                raise ValueError('год должен входить в период от 1874 до 2050')
    except ValueError as er:
        database_manager.set_status_years(status_user=status_user, status=False)
        raise ValueError(str(er))
    database_manager.set_years(status_user=status_user, years='-'.join(years))
    database_manager.set_status_years(status_user, False)
    return None


def cmd_count_films(message: Message, user: Users, status_user: CustomsStatus) -> list or None:
    """
    Функция изменяет переменную count_films в CustomsStatus пользователя, и проверяет её.
    Если проверка не успешна вернёт ошибку
    """
    if not status_user.status_count_films:
        database_manager.set_status_count_films(status_user, True)
        return [
            'Сколько фильмов показать? По умолчанию 10\n'
            '/clear - отчистка фильтра\n'
            '/return - вернутся назад\n'
        ]
    if message.text == '/clear':
        database_manager.set_count_films(status_user=status_user, count_film=DatabaseManager.default_count_films)
        database_manager.set_status_count_films(status_user=status_user, status=False)
        return None
    if message.text == '/return':
        database_manager.set_status_count_films(status_user=status_user, status=False)
        return None
    try:
        try:
            count_film = int(message.text.lower().strip(' ').strip(','))
        except ValueError:
            raise ValueError('Не правильно количество фильмов')
        if 20 < count_film or count_film <= 0:
            raise ValueError('Количество фильмов должно быть больше нуля и не больше 20')
    except ValueError as er:
        database_manager.set_status_count_films(status_user=status_user, status=False)
        raise ValueError(str(er))
    database_manager.set_count_films(status_user=status_user, count_film=count_film)
    database_manager.set_status_count_films(status_user, False)
    return None


def cmd_custom(message: Message, user: Users) -> list:
    """
    Команда custom. Изменяет состояние нахождение пользователя в команде.
    Делает запрос на kinoposk api с заданными переменными CustomsStatus
    При успешном ответе возвращает список сообщений с фильмами и заносит запрос в историю пользователя
    """
    # Получаем статусы пользователя и переменные из базы данных
    status_user: CustomsStatus = database_manager.get_customs_status(user=user)
    # Меняем значения статуса нахождения пользователя в редакторе
    if (status_user.status_custom and message.text == '/return' and not status_user.status_genres
            and not status_user.status_years and not status_user.status_count_films):
        database_manager.set_custom_status(status_user=status_user, status=False)
        return [cmd_help(message, user)]
    if not status_user.status_custom:
        database_manager.set_custom_status(status_user=status_user, status=True)

    # Запрос на изменение фильтра
    er_text = ''
    try:
        if message.text == '/genre' or status_user.status_genres:
            answer = cmd_custom_genres(message, user, status_user)
            if answer is not None:
                return answer
        if message.text == '/years' or status_user.status_years:
            answer = cmd_custom_years(message, user, status_user)
            if answer is not None:
                return answer
        if message.text == '/count_films' or status_user.status_count_films:
            answer = cmd_count_films(message, user, status_user)
            if answer is not None:
                return answer
    except ValueError as er:
        LoggerManager.logging(user=user, message=message, command='/custom {}'.format(er))
        er_text = '\n\n{}'.format(er)

    # Запрос на Кинопоиск API
    if message.text == '/get_films':
        database_manager.set_custom_status(status_user=status_user, status=False)
        params = {
            'sortField': 'rating.kp',
            'sortType': '-1',
            'type': 'movie',
            'notNullFields': ['poster.url', 'name'],
            'movieLength': '60-200',
            'limit': '{}'.format(status_user.count_films),
        }
        if status_user.genres != DatabaseManager.default_genres:
            params['genres.name'] = status_user.genres.split(', ')
        if status_user.years != DatabaseManager.default_years:
            params['year'] = status_user.years
        try:
            data = kinopoisk_api.get_answer(params=params, url=kinopoisk_api.url_movie)
        except ConnectionError as er:
            LoggerManager.logging(user=user, message=message, command='/custom {}'.format(er))
            return [er] + cmd_help(message=message, user=user)
        data_history = '/custom [{genre}, {years}, {count_films}]'.format(
            genre=status_user.genres, years=status_user.years, count_films=status_user.count_films
        )

        LoggerManager.logging(user=user, message=message, command=data_history)
        DatabaseHistoryManager.set_history_user(user=user, data_history=data_history)
        return formed_data.form_films_data_list(data) + help_message

    return [
        'Установка фильтров:\n\n'
        '/genre - установить фильтр по жанрам\n'
        '/years - установить фильтр по годам\n'
        '/count_films - установить количество фильмов, которые будет показаны\n\n'
        'Жанры: {genre}\n'
        'Год: {years}\n'
        'Количество фильмов: {count_films}\n\n'
        '/get_films - Выполнить запрос.\n'
        '/return - Вернутся назад.'
        '{er_text}'.format(
            genre=status_user.genres,
            years=status_user.years,
            count_films=status_user.count_films,
            er_text=er_text
        )
    ]


def cmd_history(message: Message, user: Users) -> list:
    """
    Возвращает список сообщений с историей запросов пользователя
    """
    answer = '\n'.join(DatabaseHistoryManager.get_history_list(user=user))
    LoggerManager.logging(user=user, message=message, command='/history')
    DatabaseHistoryManager.set_history_user(user=user, data_history='/history')
    return [answer] + help_message


class BotCommands:
    commands = {
        '/hello': cmd_start_hello,
        '/start': cmd_start_hello,
        '/help': cmd_help,
        '/low': cmd_low,
        '/high': cmd_high,
        '/custom': cmd_custom,
        '/history': cmd_history,
    }

    @classmethod
    def user_commands(cls, message: Message, user: Users) -> list:
        if database_manager.check_customs_status(user):
            return cmd_custom(message, user)
        func_answer = BotCommands.commands.get(message.text)
        if func_answer is not None:
            return func_answer(message, user)
        return ['Не определили команду.\nВведите /help для просмотра доступных команд.']
