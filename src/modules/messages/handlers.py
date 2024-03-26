from loguru import logger
from pyrogram.types import Message

from models.dto import SignalMessage
from modules.messages.parsers import message_parser
from modules.orders.orders_service import order_service


async def handle_signal(origin: Message, message: SignalMessage):
    if signal := message_parser.get_signal(message):
        try:
            result = order_service.make_order_by_signal(signal)
            await origin.reply(
                text=f"Order was created:\n```json\n{result.json()}\n```",
                reply_to_message_id=origin.id,
            )
        except Exception as e:
            await origin.reply(
                text=f"Order was not created\n```\n{e}\n```",
                reply_to_message_id=origin.id,
            )
    else:
        warn = f"No signal. Message: {message.text}"
        logger.warning(warn)
        await origin.reply(text=warn, reply_to_message_id=origin.id)
