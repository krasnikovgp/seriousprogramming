from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, Filters, ConversationHandler, MessageHandler, CommandHandler
from db import write_to_db, find_user_by_id

import logging

logger = logging.getLogger(__name__)

WAIT_NAME, WAIT_SURNAME, WAIT_BD, WAIT_OK = range(4)


def check_register(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    user_id = update.message.from_user.id
    logger.info(f'{username=} Вызвал функцию check_reg')
    user = find_user_by_id(user_id)
    if not user:
        return ask_name(update, context)

    answer = [
        'Привет! Ты уже зарегистрирован со следующими данными : ',
        f'Имя : {user[1]}',
        f'Фамилия : {user[2]}',
        f'Дата Рождения : {user[3]}'
    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())


def get_yes_no(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info(f'{username=} Вызвал функцию ask_yes_no')


def ask_name(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info(f'{username=} Вызвал функцию ask_name')
    text = 'Напиши свое имя :'

    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())

    return WAIT_NAME


def get_name(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['name'] = text
    answer = f'Твое имя - {text}'
    update.message.reply_text(answer)

    return ask_surname(update, context)


def ask_surname(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info(f'{username=} Вызвал функцию ask_surname')
    text = 'Напиши свою фамилию :'

    update.message.reply_text(text)

    return WAIT_SURNAME


def get_surname(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['surname'] = text
    answer = f'Твоя фамилия - {text}'
    update.message.reply_text(answer)

    return ask_bd(update, context)


def ask_bd(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    logger.info(f'{username=} Вызвал функцию ask_bd')
    text = 'Напиши свою дату рождения :'

    update.message.reply_text(text)

    return WAIT_BD


def get_bd(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['bd'] = text
    answer = f'Твоя дата рождения - {text}'
    update.message.reply_text(answer)

    return register(update, context)


def register(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    user_id = update.effective_user.id
    logger.info(f'{username} вызвал команду register')

    name = context.user_data['name']
    surname = context.user_data['surname']
    birthday = context.user_data['bd']

    write_to_db(user_id, name, surname, birthday)
    answer = [
        'Зареган!',
        'Твои данные:',
        f'Имя : {name}', f'Фамилия : {surname}', f'Дата Рождения : {birthday}'
    ]
    answer1 = '\n'.join(answer)

    update.message.reply_text(answer1)
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