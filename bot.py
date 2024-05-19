"""Create a bot object"""
from telebot import TeleBot
from telebot.types import Message

from config import access_token
from content.messages import messages
from database.connect import database
from utils import check_link, generate_event_message


bot = TeleBot(access_token, parse_mode='HTML')


@bot.message_handler(commands=['start', 'help'])
def start_help_handler(message: Message) -> None:
    """
    :param message:
    :return:
    """
    bot.send_message(message.chat.id, messages[message.text[1:]])


@bot.message_handler(commands=['get_article'])
def get_article_handler(message: Message) -> None:
    """
    :param message:
    :return:
    """
    random_link = database.get_random_link(message.chat.id)

    if random_link:
        bot.send_message(message.chat.id,
                         messages['get_article_default'].format(
                             article=random_link))
    else:
        bot.send_message(message.chat.id, messages['get_article_failure'])


@bot.message_handler(commands=['get_history'])
def het_history_handler(message: Message) -> None:
    """
    :param message:
    :return:
    """
    bot.send_message(message.chat.id, generate_event_message(
        database.get_event_list(message.chat.id)))


@bot.message_handler(func=lambda message: check_link(message.text))
def save_article_handler(message: Message) -> None:
    """
    :param message:
    :return:
    """
    if database.save_link(message.chat.id, message.text):
        bot.send_message(message.chat.id, messages['save_article_default'])
    else:
        bot.send_message(message.chat.id, messages['save_article_failure'])


@bot.message_handler()
def unknown_case_handler(message: Message) -> None:
    """
    :param message:
    :return:
    """
    bot.send_message(message.chat.id, messages['unknown_case'])
