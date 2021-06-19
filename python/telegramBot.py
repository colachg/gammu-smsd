#!/usr/bin/env python3
# encoding: utf-8
import os
import logging
import gammu.smsd

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils.executor import start_webhook


# webhook settings
WEBHOOK_HOST = os.environ['WEBHOOK_HOST']
WEBHOOK_PATH = os.environ['CHANIFY_TOKEN']
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = 5000

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ['TELEGRAM_BOT_TOKEN'])
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm ec20 Bot!\nPowered by aiogram.")


@dp.message_handler(filters.Regexp(".* -> \d*"))
async def echo(message: types.Message):
    # Regular request
    number = int(message.text.split(' -> ')[1])
    send_sms(number, message.text.split(' -> ')[0])
    await message.reply("send successfully")
    # await bot.send_message(message.chat.id, "send successfully")


def send_sms(number, content):
    smsd = gammu.smsd.SMSD('/etc/gammu-smsdrc')
    message = {'Text': content, 'SMSC': {'Location': 1}, 'Number': number}
    smsd.InjectSMS([message])


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown
    # Remove webhook (not acceptable in some cases)
    # await bot.delete_webhook()

    # Close DB connection (if used)
    # await dp.storage.close()
    # await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

