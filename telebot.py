from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import *
import logging
from key import TOKEN
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    updater = Updater(token=TOKEN)  # Вытягиваем обновления из тг
    dispatcher: Dispatcher = updater.dispatcher  # Распределяем обновы по обработчикам

    updater.dispatcher.add_handler(CommandHandler('help', do_help))
    updater.dispatcher.add_handler(CommandHandler('start', do_start))
    updater.dispatcher.add_handler(CommandHandler('menu', do_menu))
    updater.dispatcher.add_handler(CommandHandler('menu2', do_inline_keyboard))
    updater.dispatcher.add_handler(CommandHandler('getcat', get_cat))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, do_echo))

    updater.start_polling()
    logger.info(updater.bot.getMe())
    updater.idle()


def do_echo(update, context):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    text = update.message.text

    logger.info(f'{username=} {user_id=} Вызвал функцию do_echo')
    answer = [
        f'Твой {username=}',
        f'Твой id = {user_id}',
        f'Ты написал "{text}"'
    ]
    answer = '\n'.join(answer)

    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())


def do_start(update, context):
    user_id = update.message.from_user.id
    user_fullname = update.message.from_user.full_name
    logger.info(f'{user_id} вызвал функцию do_start')
    text = [
        f'Здарова, {user_fullname}!',
        f'У меня теперь есть твой {user_id=}',
        'Напиши /menu, чтобы узнать, что я умею :)'
    ]
    text = '\n'.join(text)
    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())


def do_menu(update, context):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} вызвал меню')
    buttons = [
        ['/help', '/getcat'],
        ['weather in Moscow'],
        ['real time in USA']
    ]
    text = 'Выберите кнопку :)'
    keyboard = ReplyKeyboardMarkup(buttons)
    update.message.reply_text(text, reply_markup=keyboard)


def do_help(update, context):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} вызвал команду do_help')
    text = [
        f'У меня есть разные команды:',
        f'/menu, /getcat (остальное в разработке)',
        f'Также у меня есть функция ECHO'
    ]
    text = '\n'.join(text)
    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Друг, у меня такого нет :(", reply_markup=ReplyKeyboardRemove())


def do_inline_keyboard(update, context):
    user_id = update.message.from_user.id
    logger.info(f"{user_id=} Bызвaл функцию do_inline_keyboard")
    buttons = [
        ['/help', '/getcat'],
        ['weather in Moscow'],
        ['real time in USA']
    ]
    keyboard_button = [[InlineKeyboardButton(text=text, callback_data=text) for text in row] for row in buttons]
    keyboard = InlineKeyboardMarkup(keyboard_button)
    text = "Выбери одну из кнопочек :)"
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )


ERROR_MESSAGE = 'Ошибка при запросе к основному API: {error}'
URL = 'https://api.thecatapi.com/v1/images/search'
DOGS_URL = 'https://api.thedogapi.com/v1/images/search'
RESPONSE_USERNAME = 'Картинку {image_name} запросил: {username}, {name}'


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(ERROR_MESSAGE.format(error=error))
        new_url = DOGS_URL
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def get_cat(update, context):
    chat = update.effective_chat
    logging.info(RESPONSE_USERNAME.format(
        image_name='котека',
        username=update.message.chat.username,
        name=update.message.chat.first_name
    ))
    context.bot.send_photo(chat.id, get_new_image())


if __name__ == '__main__':
    main()
