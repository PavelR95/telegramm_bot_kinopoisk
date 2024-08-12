import requests
import os
from typing import Dict
from dotenv import load_dotenv


class KinoApi:

    def __init__(self):
        """
        base_url: базовый url для обращения к API
        url_movie: дополнительный url для универсального поиска фильмов
        url_possible: дополнительный url для получения всех жанров и типов, не используется на данный момент
        headers: обязательный заголовок, в него заносится обязательное поле X-API-KEY
        """
        load_dotenv()
        self.token = os.getenv('TOKEN_KP')
        self.base_url = 'https://api.kinopoisk.dev'
        self.url_movie = '/v1.4/movie'
        self.url_possible = '/v1/movie/possible-values-by-field'
        self.headers = {
            'accept': 'application/json',
            'X-API-KEY': self.token,
        }

    def request_get(self, url: str, params: dict) -> Dict:
        """
        Выполняет запрос и возвращает ответ в виде словаря.
        Ключи:
            connection: Определяет было ли подключение
            error: текст ошибки, None если ошибки не было
            data: данные в json формате
        :param url: конечная точка запроса
        :param params: передающие параметры
        :return: dict возвращает словарь с ответом от сервера и данными
        """
        answer = {
            'error': None,
            'data': None,
        }
        try:
            response = requests.get(self.base_url + url, headers=self.headers, params=params)
            if response.status_code == 400:
                raise ValueError('\n'.join(response.json()['message']))
            answer['data'] = response.json()
        except requests.exceptions.ConnectionError:
            answer['error'] = 'Ошибка соединения с Кинопоиском, обратитесь к администратору.'
        except requests.exceptions.JSONDecodeError:
            answer['error'] = 'Ошибка: данные не были получены.'
        except ValueError as er:
            answer['error'] = 'Один или несколько параметров переданы неверно:\n{}'.format(er)
        finally:
            return answer

    def get_answer(self, params, url) -> dict:
        """
        Универсальный метод запроса.
        Вызывает ошибку ConnectionError если ответ пришёл с полем error не None и передаёт в неё текст.
        :param params: Параметры для запроса
        :param url: Дополнительный url для поиска
        :return: возвращает словарь с данными или None, если была ошибка.
        """
        answer = self.request_get(url=url, params=params)
        if answer['error'] is not None:
            raise ConnectionError(answer['error'])
        return answer['data']
