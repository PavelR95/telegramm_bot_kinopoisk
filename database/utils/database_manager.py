from peewee import DoesNotExist
from database.common.models import Users, CustomsStatus, History


class DatabaseManager:
    default_genres = 'Любые жанры'
    default_years = 'Любые года'
    default_count_films = 10

    @classmethod
    def create_get_user(cls, id_telegram: int) -> Users:
        """Добавляет нового пользователя если его нет.
        Создаёт связные с ним таблицы: CustomsStatus, History"""
        try:
            user: Users = Users.get(Users.id_telegram == id_telegram)
            return user
        except DoesNotExist:
            user = Users(id_telegram=id_telegram)
            user.save()
            print('New User: {}'.format(user.id_telegram))
            DatabaseManager.check_create_status(user)
            DatabaseManager.check_create_history(user)
            return user

    @classmethod
    def check_create_status(cls, user: Users):
        """Создаёт таблицу статусов если её нет"""
        try:
            CustomsStatus.get(CustomsStatus.user == user)
        except DoesNotExist:
            status = CustomsStatus(
                user=user,
                status_custom=False,
                status_genres=False,
                status_years=False,
                status_count_films=False,
                genres=DatabaseManager.default_genres,
                years=DatabaseManager.default_years,
                count_films=DatabaseManager.default_count_films
            )
            status.save()
            print('Создаю статус')

    @classmethod
    def check_create_history(cls, user: Users):
        """Создаёт таблицу истории если её нет"""
        try:
            History.get(History.user == user)
        except DoesNotExist:
            history = History(
                user=user,
                history='',
            )
            history.save()
            print('Создаю историю')

    @classmethod
    def check_customs_status(cls, user: Users) -> bool:
        """Возвращает состояние нахождения пользователя в команде custom пользователя"""
        status: CustomsStatus = CustomsStatus.get(CustomsStatus.user == user)
        return status.status_custom

    @classmethod
    def get_customs_status(cls, user: Users) -> CustomsStatus:
        """Возвращает объект таблицы CustomsStatus"""
        custom_status: CustomsStatus = CustomsStatus.get(CustomsStatus.user == user)
        return custom_status

    @classmethod
    def info_user(cls, user: Users):
        """Выводит информацию о пользователе"""
        custom_status = DatabaseManager.get_customs_status(user=user)
        print(
            'User id: {user_id}; tg_id: {tg_id}; status_custom: {status_custom}'.format(
                user_id=user.id_user, tg_id=user.id_telegram, status_custom=custom_status.status_custom
            )
        )

    @classmethod
    def set_custom_status(cls, status_user: CustomsStatus, status: bool):
        """Изменение состояние пользователя CustomsStatus.status_custom"""
        status_user.status_custom = status
        status_user.save()

    @classmethod
    def set_status_genres(cls, status_user: CustomsStatus, status: bool):
        """Изменение состояние пользователя CustomsStatus.status_genres"""
        status_user.status_genres = status
        status_user.save()

    @classmethod
    def set_genres(cls, status_user: CustomsStatus, genres: str):
        """Изменение переменной пользователя команды custom CustomsStatus.genres"""
        status_user.genres = genres
        status_user.save()

    @classmethod
    def set_status_years(cls, status_user: CustomsStatus, status: bool):
        """Изменение состояние пользователя CustomsStatus.status_years"""
        status_user.status_years = status
        status_user.save()

    @classmethod
    def set_years(cls, status_user: CustomsStatus, years: str):
        """Изменение переменной пользователя команды custom CustomsStatus.years"""
        status_user.years = years
        status_user.save()

    @classmethod
    def set_status_count_films(cls, status_user: CustomsStatus, status: bool):
        """Изменение состояние пользователя CustomsStatus.status_count_films"""
        status_user.status_count_films = status
        status_user.save()

    @classmethod
    def set_count_films(cls, status_user: CustomsStatus, count_film: int):
        """Изменение переменной пользователя команды custom CustomsStatus.count_films"""
        status_user.count_films = count_film
        status_user.save()
