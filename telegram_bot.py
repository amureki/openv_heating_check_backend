# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os

from telegram import Updater

from reading_sensors import run_vclient


TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


def temperature(bot, update):
    temp = run_vclient('getTempA', update=False)
    if temp is not 'err':
        text = 'Current office temperature is {}°C'.format(round(temp, 1))
    else:
        text = 'Our sensors gone for lunch, try again later'
    bot.sendMessage(chat_id=update.message.chat_id, text=text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    dispatcher.addTelegramCommandHandler('temperature', temperature)
    updater.start_polling()
