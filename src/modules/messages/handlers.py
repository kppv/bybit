from loguru import logger
from pyrogram import Client
from pyrogram.types import Message

from conf.settings import settings
from models.dto import SignalMessage
from modules.messages.parsers import message_parser
from modules.orders.orders_service import order_service


async def handle_signal(client: Client, origin: Message, message: SignalMessage):
    if signal := message_parser.get_signal(message):
        try:
            result = order_service.make_order_by_signal(signal)
            await client.send_message(
                text=f"Order was created:\n```json\n{result.json()}\n```",
                reply_to_message_id=origin.id,
                chat_id=int(settings.reply_chat_id),
            )
        except Exception as e:
            await client.send_message(
                text=f"Order was not created\n```\n{e}\n```",
                reply_to_message_id=origin.id,
                chat_id=int(settings.reply_chat_id),
            )
    else:
        warn = f"No signal. Message: {message.text}"
        logger.warning(warn)
        await client.send_message(
            chat_id=int(settings.reply_chat_id),
            text=warn,
            reply_to_message_id=origin.id,
        )
