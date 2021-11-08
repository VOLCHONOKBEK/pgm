from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from pyrogram.raw import functions
from pyrogram.raw.types import InputPeerUser
from .utils.utils import modules_help, prefix
from .utils.db import db


async def anti_pm_handler(client: Client, message: Message):
    status = await db.get('core.antipm', 'status', False)
    if status:
        if message.chat.type in ["private"]:
            if not message.from_user.is_contact \
                    and not message.from_user.is_bot \
                    and not message.from_user.is_self:
                await client.read_history(message.chat.id)
                user_info = await client.resolve_peer(message.chat.id)
                await message.delete()
                await client.send(functions.messages.ReportSpam(peer=(user_info)))
                await client.send(functions.messages.DeleteHistory(peer=(user_info),
                                                                   max_id=0,
                                                                   revoke=True))


@Client.on_message(filters.command(["anti_pm"], prefix) & filters.me)
async def anti_pm(client: Client, message: Message):
    status = await db.get('core.antipm', 'status', False)
    if status:
        await message.edit("Anti-pm enabled")
        my_handler = MessageHandler(anti_pm_handler,
                                    filters.private)
        client.add_handler(my_handler)
    else:
        await db.set('core.antipm', 'status', True)
        my_handler = MessageHandler(anti_pm_handler,
                                    filters.private)
        client.add_handler(my_handler)
        await message.edit("Anti-pm enabled")


@Client.on_message(filters.command(["disable_anti_pm"], prefix) & filters.me)
async def disable_anti_pm(client: Client, message: Message):
    await db.set('core.antipm', 'status', False)
    await message.edit("Anti-pm disabled")


modules_help.update({
                        'antipm': '''anti_pm - Delete all messages from users who are not in the contact book, disable_anti_pm - Disable''',
                        'antipm module': 'AntiPm: anti_pm, '
                                         'disable_anti_pm\n'})
