from database.common.models import BaseModel, database


class DataBase:

    def __init__(self):
        self.database = database

    def create_database(self):
        self.database.create_tables([_class for _class in BaseModel.__subclasses__()])
