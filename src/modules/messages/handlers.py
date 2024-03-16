from models.dto import SignalMessage
from modules.messages.parsers import message_parser
from modules.orders.orders_service import order_service


async def handle_signal(message: SignalMessage):
    if signal := message_parser.get_signal(message):
        await order_service.make_order_by_signal(signal)
