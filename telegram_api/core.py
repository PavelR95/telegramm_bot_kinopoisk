import telebot
import os

from telebot.types import Message
from dotenv import load_dotenv

from .utils.answer import get_answer
from .utils.bot_commands import BotCommands
from database.utils.database_manager import DatabaseManager


class TgBot:
    """
    Класс описывает основные функции TgBot,
    command обрабатывает команды пользователя и отправляет ответ,
    answer обрабатывает сообщения и отправляет ответ,
    start_bot запускает бота.
    """

    def __init__(self):
        """
        При инициализации бота принимает токен и создаёт объект telebot.TeleBot.
        Для обработки команд инициализирует BotCommands.
        Для обращения к сторонним плагинам создаёт словарь __plugins
        Так же обрабатывает приходящие сообщения.
        """
        load_dotenv()
        self.__token = os.getenv('TOKEN_TG')
        self.bot = telebot.TeleBot(self.__token)
        self.database_manager = DatabaseManager()
        self.bot_commands = BotCommands()

        @self.bot.message_handler(func=lambda message: True)
        def answer(message: Message):
            """
            Заносит в базу данных пользователя, если там такого нет.
            Формирует ответ на сообщение пользователя.
            Определяет, введена ли команда. Если команда введена,
            ответ получает при помощи модуля bot_commands
            Ответ на сообщения получает при помощи модуля utils.answer
            Ответ формируется в виде списка строк, которые необходимо отправить пользователю
            """
            # Проверяем и получаем объект пользователя в базе данных
            user = self.database_manager.create_get_user(message.chat.id)
            # Обрабатываем сообщение
            text_message = message.text.lower()
            if text_message.startswith('/') or self.database_manager.check_customs_status(user=user):
                message_list = self.bot_commands.user_commands(message, user)
            else:
                message_list = [get_answer(message, self.bot)]
            for message_text in message_list:
                self.bot.send_message(message.chat.id, message_text)

    def start_bot(self):
        self.bot.infinity_polling()
