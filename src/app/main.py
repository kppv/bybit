from loguru import logger
from pyrogram import Client
from pyrogram.types import Message

from conf.settings import settings
from modules.handler.message_handler import MessageHandler
from modules.models.dto import SignalMessage

app = Client("my_account", settings.api_id, settings.api_hash)
message_handler = MessageHandler()


@app.on_message()
async def handler(client: Client, message: Message):
    if message.chat.id == int(settings.chat_id):
        logger.info(f"Message from {message.chat.id}: {message}")
        await message_handler.handle(SignalMessage.from_orm(message))


app.run()
