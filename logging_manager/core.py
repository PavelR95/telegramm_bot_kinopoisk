import logging
import os
from dotenv import load_dotenv
from database.common.models import Users
from telebot.types import Message

load_dotenv()

logging.basicConfig(level=logging.INFO, filename=os.getenv('LOGGING_FILE'), filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


class LoggerManager:
    @classmethod
    def logging(cls, user: Users, message: Message, command: str):
        log_message = ('\nUser_database_id: {user_id}; User_tg_id: {telegram_id}; '
                       'message: {message_text};, command: {command}').format(
            user_id=user.id_user,
            telegram_id=user.id_telegram,
            message_text=message.text,
            command=command
        )
        logging.info(log_message)
        pass
