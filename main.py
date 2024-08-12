from telegram_api.core import TgBot
from database.core import DataBase


def main():
    db = DataBase()
    db.create_database()
    bot = TgBot()
    bot.start_bot()


if __name__ == '__main__':
    main()
