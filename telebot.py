from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import *
import logging
from settings import TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    updater = Updater(token=TOKEN)  # Вытягиваем обновления из тг
    dispatcher: Dispatcher = updater.dispatcher  # Распределяем обновы по обработчикам

    echo_handler = MessageHandler(Filters.text, do_echo)
    start_handler = CommandHandler('start', do_start)
    keyboard_handler = CommandHandler('keyboard', do_keyboard)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    logger.info(updater.bot.getMe())
    updater.idle()


def do_echo(update: Update, context: CallbackContext):
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


def do_start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_fullname = update.message.from_user.full_name
    logger.info(f'{user_id} вызвал функцию do_start')
    text = [
        f'Здарова, {user_fullname}!',
        f'У меня теперь есть твой {user_id=}',
        'Я знаю команды /start, /keyboard'
        ]
    text = '\n'.join(text)
    update.message.reply_text(text)


def do_keyboard(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} вызвал клавиатуру')
    buttons = [
        ['one', 'two'],
        ['weather in Moscow'],
        ['real time in USA']
    ]
    text = 'Выберите кнопку :)'
    keyboard = ReplyKeyboardMarkup(buttons)
    update.message.reply_text(text, reply_markup=keyboard)


if __name__ == '__main__':
    main()
