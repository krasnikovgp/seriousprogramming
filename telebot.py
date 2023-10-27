from telegram import *
from telegram.ext import *
import logging
from key import TOKEN
import requests
import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    updater = Updater(token=TOKEN)  # Вытягиваем обновления из тг
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('help', do_help))
    dp.add_handler(CommandHandler('start', do_start))
    dp.add_handler(CommandHandler('menu', do_menu))
    dp.add_handler(CommandHandler('ikmenu', do_inline_keyboard))
    dp.add_handler(CommandHandler('getcat', get_cat))
    dp.add_handler(CommandHandler('set_timer', set_timer))
    dp.add_handler(CommandHandler('stop_timer', delete_timer))
    dp.add_handler(CommandHandler('getdog', get_dog))
    dp.add_handler(CallbackQueryHandler(keyboard_react))
    dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_handler(MessageHandler(Filters.text, do_echo))

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
        f'<i>Здравствуй, {user_fullname}!</i>',
        f'<i>У меня теперь есть твой <b>юзерайди</b></i> = <code>{user_id}</code>',
        f'',
        '<i>Напиши /menu, чтобы узнать, что <b>я умею</b></i> :)'
    ]
    text = '\n'.join(text)
    update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())


def do_menu(update, context):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} вызвал меню')
    buttons = [
        ['/help', '/getcat'],
        ['weather in Moscow'],
        ['/set_timer', '/stop_timer'],
        ['/ikmenu']
    ]
    text = 'Выберите кнопку :)'
    keyboard = ReplyKeyboardMarkup(buttons)
    update.message.reply_text(text, reply_markup=keyboard)


def do_help(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    logger.info(f'{user_id=} вызвал команду do_help')
    text = [
        f'<i>У меня есть разные <b>команды</b></i>:',
        f'/menu',
        f'/getcat',
        f'/ikmenu',
        f'<i>Также у меня есть функция</i>  <code>ECHO</code>'
    ]
    text = '\n'.join(text)
    context.bot.send_message(update.effective_chat.id, text, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())


def unknown(update, context):
    context.bot.reply_text(chat_id=update.effective_chat.id,
                           text="Друг, у меня такого нет :(",
                           reply_markup=ReplyKeyboardRemove())


def do_inline_keyboard(update, context):
    user_id = update.message.from_user.id
    logger.info(f"{user_id=} Bызвaл функцию do_inline_keyboard")
    buttons = [
        ['getcat', 'getdog'],
        ['help'],
        ['set_timer', 'stop_timer']
    ]
    keyboard_button = [[InlineKeyboardButton(text=text, callback_data=text) for text in row] for row in buttons]
    keyboard = InlineKeyboardMarkup(keyboard_button)
    text = "Выбери одну из кнопочек :)"
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )


def keyboard_react(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = update.effective_user.id
    logger.info(f'{user_id=} вызвал функцию keyboard_react')
    if query.data == 'getcat':
        get_cat(update, context)
    if query.data == 'getdog':
        get_dog(update, context)
    if query.data == 'set_timer':
        set_timer(update, context)
    if query.data == 'stop_timer':
        delete_timer(update, context)
    if query.data == 'help':
        do_help(update, context)


def set_timer(update, context):
    logger.info(f'Выполнена функция {set_timer}')
    user_id = update.effective_user.id
    context.bot_data["user_id"] = user_id
    context.bot_data["timer"] = datetime.datetime.now()
    context.bot_data['timer_job'] = context.job_queue.run_repeating(show_seconds, 1)
    context.bot.send_message(user_id, 'Таймер запущен! \n'
                                      'Нажмите /stop_timer, чтобы остановить таймер :)')


def show_seconds(context: CallbackContext):
    logger.info(f'{context.job_queue.jobs()}')
    message_id = context.bot_data.get('message_id', None)
    user_id = context.bot_data['user_id']
    timer = datetime.datetime.now() - context.bot_data['timer']
    timer = timer.seconds
    text = f'Прошло - {timer} - секунд'
    if not message_id:
        message = context.bot.send_message(user_id, text)
        context.bot_data['message_id'] = message.message_id
    else:
        context.bot.edit_message_text(text, chat_id=user_id, message_id=message_id)


def delete_timer(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f'Выполнена функция {delete_timer}')
    context.bot_data['timer_job'].schedule_removal()
    context.bot_data.clear()
    context.bot.send_message(
        chat_id,
        f'Таймер отстановлен! \n'
        f'включи его заново командой /set_timer',
        reply_markup=ReplyKeyboardRemove())


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
        username=chat.username,
        name=chat.first_name
    ))
    context.bot.send_photo(chat.id, get_new_image(), reply_markup=ReplyKeyboardRemove())


def get_new_image2():
    try:
        response = requests.get(DOGS_URL)
    except Exception as error:
        logging.error(ERROR_MESSAGE.format(error=error))
        new_url = URL
        response = requests.get(new_url)

    response = response.json()
    random_dog = response[0].get('url')
    return random_dog


def get_dog(update, context):
    chat = update.effective_chat
    logging.info(RESPONSE_USERNAME.format(
        image_name='пес',
        username=chat.username,
        name=chat.first_name
    ))
    context.bot.send_photo(chat.id, get_new_image2(), reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    main()
