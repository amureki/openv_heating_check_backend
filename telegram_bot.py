import logging
import os

from telegram import Updater

from reading_sensors import run_vclient


TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


def temperature(bot, update):
    text = run_vclient('getTempA')
    bot.sendMessage(chat_id=update.message.chat_id, text=text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    dispatcher.addTelegramCommandHandler('temperature', temperature)
    updater.start_polling()
