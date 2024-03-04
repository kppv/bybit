from models.dto import SignalMessage
from modules.messages.parsers import MessageParser
from modules.orders.orders_service import OrderService


class MessageHandler:
    def __init__(
        self,
        message_parser: MessageParser,
        order_service: OrderService,
    ):
        super().__init__()
        self.message_parser = message_parser
        self.order_service = order_service

    async def handle(self, message: SignalMessage):
        signal = self.message_parser.get_signal(message)
        self.order_service.make_order_by_signal(signal)


message_handler = MessageHandler(MessageParser(), OrderService())
