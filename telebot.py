from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import *
import logging
from key import TOKEN

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
    menu_handler = CommandHandler('menu', do_menu)
    help_handler = CommandHandler('help', do_help)
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(menu_handler)
    dispatcher.add_handler(unknown_handler)
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
        'Напиши /menu, чтобы узнать, что я умею :)'
    ]
    text = '\n'.join(text)
    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())


def do_menu(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} вызвал меню')
    buttons = [
        ['/help', 'some'],
        ['weather in Moscow'],
        ['real time in USA']
    ]
    text = 'Выберите кнопку :)'
    keyboard = ReplyKeyboardMarkup(buttons)
    update.message.reply_text(text, reply_markup=keyboard)


def do_help(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} вызвал команду do_help')
    text = [
        f'У меня есть разные команды:',
        f'/menu (остальное в разработке)',
        f'Также у меня есть функция ECHO'
    ]
    text = '\n'.join(text)
    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())


"""
def do_clear(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} вызвал команду do_clear')
"""


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Друг, у меня такого нет :(")


if __name__ == '__main__':
    main()
