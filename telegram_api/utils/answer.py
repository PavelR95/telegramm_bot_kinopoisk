from telebot.types import Message
from telebot import TeleBot

# Словарь с ответами.
answer = {
    'привет': 'Привет, {name}, Моё имя @{name_bot}'.format,
}


def get_answer(message: Message, bot: TeleBot):
    """
    Принимает на вход сообщение от пользователя и формирует ответ
    :param bot:
    :param message: telebot.types.Message: сообщение от пользователя
    :return: str: ответ пользователю
    """
    name_user = message.chat.first_name
    bot_info = bot.get_me()
    text_answer = answer.get(message.text.lower())
    if text_answer is None:
        return 'Простите я не знаю что вам сказать'
    else:
        return text_answer(name=name_user, name_bot=bot_info.username)

