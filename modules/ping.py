from pyrogram.types import Message
from pyrogram import filters
from utils import app
import datetime


@app.on_message(filters.command('ping', ['.']) & filters.me)
def ping(client, message):
    start = datetime.datetime.now()
    message.edit('Pong')
    end = datetime.datetime.now()
    ping = (end - start).microseconds / 1000
    message.edit('Ping\n <code>{}</code>'.format(ping))

    