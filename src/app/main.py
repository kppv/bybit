from loguru import logger
from pyrogram import Client
from pyrogram.types import Message

from conf.settings import settings
from models.dto import SignalMessage
from modules.messages.handlers import handle_signal

# 337327418
app = Client(name="my_account", api_id=settings.app_id, api_hash=settings.api_hash)


@app.on_message()
async def handler(client: Client, message: Message):
    if message.chat.id in settings.chat_id and not message.forward_from_chat:
        logger.info(f"Message from {message.chat.id}: {message.text}")
        await handle_signal(client, message, SignalMessage.from_orm(message))


if __name__ == "__main__":
    logger.info(f"Started with settings: {settings.json()}")
    app.run()
