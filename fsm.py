from telegram import Update
from telegram.ext import CallbackContext, Filters, ConversationHandler, MessageHandler, CommandHandler

import logging

logger = logging.getLogger(__name__)

WAIT_NAME, WAIT_SURNAME, WAIT_BD = range(3)


def ask_name(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info(f'{username=} Вызвал функцию ask_name')
    text = 'Напиши свое имя :'

    update.message.reply_text(text)

    return WAIT_NAME


def get_name(update: Update, context: CallbackContext):
    text = update.message.text

    answer = f'Твое имя - {text}'
    update.message.reply_text(answer)

    return ask_surname


def ask_surname(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info(f'{username=} Вызвал функцию ask_surname')
    text = 'Напиши свое имя :'

    update.message.reply_text(text)

    return WAIT_SURNAME


def get_surname(update: Update, context: CallbackContext):
    text = update.message.text

    answer = f'Твоя фамилия - {text}'
    update.message.reply_text(answer)

    return ask_bd


def ask_bd(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info(f'{username=} Вызвал функцию ask_bd')
    text = 'Напиши свою дату рождения :'

    update.message.reply_text(text)

    return WAIT_BD


def get_bd(update: Update, context: CallbackContext):
    text = update.message.text

    answer = f'Твоя дата рождения - {text}'
    update.message.reply_text(answer)

    return register


def register(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info(f'{username} вызвал команду register')
    answer = 'Зареган!'
    update.message.reply_text(answer)

    return ConversationHandler.END


register_handler = ConversationHandler(
    entry_points=[CommandHandler('register', ask_name)],
    states={
        WAIT_NAME: [MessageHandler(Filters.text, get_name)],
        WAIT_SURNAME: [MessageHandler(Filters.text, get_surname)],
        WAIT_BD: [MessageHandler(Filters.text, get_bd)]
    },
    fallbacks=[]
)
