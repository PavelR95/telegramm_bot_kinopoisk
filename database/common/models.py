import os
from dotenv import load_dotenv

import peewee as pw

load_dotenv()
database_path = os.getenv('DATABASE')

# Создаём базу данных
database = pw.SqliteDatabase(database_path)


class BaseModel(pw.Model):
    """Определим базовую модель базы данных"""

    class Meta:
        database = database


class Users(BaseModel):
    """Модель таблицы пользователей"""
    id_user = pw.IntegerField(primary_key=True, null=False)
    id_telegram = pw.IntegerField(null=False)


class CustomsStatus(BaseModel):
    """Модель таблицы статусов пользователй"""
    user = pw.ForeignKeyField(Users, related_name='custom_status')
    status_custom = pw.BooleanField()
    status_genres = pw.BooleanField()
    status_years = pw.BooleanField()
    status_count_films = pw.BooleanField()
    genres = pw.CharField()
    years = pw.CharField()
    count_films = pw.IntegerField()


class History(BaseModel):
    """Модель таблицы статусов пользователй"""
    user = pw.ForeignKeyField(Users, related_name='stat')
    history = pw.CharField()
