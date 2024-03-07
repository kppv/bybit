from models.dto import SignalMessage
from modules.messages.parsers import message_parser
from modules.orders.orders_service import order_service


async def handle_signal(message: SignalMessage):
    signal = message_parser.get_signal(message)
    order_service.make_order_by_signal(signal)
