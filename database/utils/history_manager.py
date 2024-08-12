import datetime
from database.common.models import Users, History


class DatabaseHistoryManager:
    @classmethod
    def get_history_obj(cls, user: Users) -> History:
        """Возвращает объект History"""
        return History.get(History.user == user)

    @classmethod
    def get_history_list(cls, user: Users) -> list:
        """Возвращает историю пользователя в виде списка"""
        # Получаем объект истории пользователя
        history = DatabaseHistoryManager.get_history_obj(user=user)
        # Получаем строку истории пользователя
        user_history_str: str = history.history
        if user_history_str == '':
            return ['Нет истории']
        # Возвращаем историю пользователя в виде списка.
        return user_history_str.split('; ')

    @classmethod
    def set_history_user(cls, user: Users, data_history: str):
        """Сохраняет историю пользователя, Ограничение не больше 5 записей"""
        # Получаем объект истории пользователя
        history: History = DatabaseHistoryManager.get_history_obj(user=user)
        # Получаем список истории пользователя
        if history.history == '':
            user_history_list = []
        else:
            user_history_list: list = DatabaseHistoryManager.get_history_list(user=user)
        # проверяем ограничение
        if len(user_history_list) == 5:
            user_history_list.pop(0)
        # Формируем запись
        history_str = '{date} {user_history}'.format(
            date=datetime.datetime.today().strftime('%d-%m-%Y'),
            user_history=data_history
        )
        # Добавляем в список
        user_history_list.append(history_str)
        # Сохраняем базу данных
        history.history = '; '.join(user_history_list)
        history.save()
