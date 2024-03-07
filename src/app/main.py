from loguru import logger
from pyrogram import Client
from pyrogram.types import Message

from conf.settings import settings
from models.dto import SignalMessage
from modules.messages.handlers import handle_signal

app = Client("my_account", settings.api_id, settings.api_hash)


@app.on_message()
async def handler(client: Client, message: Message):
    if message.chat.id == int(settings.chat_id):
        logger.info(f"Message from {message.chat.id}: {message}")
        await handle_signal(SignalMessage.from_orm(message))


app.run()
