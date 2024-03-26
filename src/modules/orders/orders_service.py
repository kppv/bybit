from loguru import logger

from models.dto import BaseSignal, Order
from modules.bybit.client import bybit_client
from modules.core.core import ExchangeClient
from modules.orders.orders_strategies import get_strategy


class OrderService:
    def __init__(self, client: ExchangeClient):
        self.client = client

    def make_order_by_signal(self, signal: BaseSignal) -> Order:
        strategy = get_strategy(signal, self.client)
        try:
            logger.info(f"Strategy [{type(strategy).__name__}] try to create order")
            result = strategy.create_order()
            logger.info(f"Order was created: {result}")
            return result
        except Exception as e:
            logger.error(f"No order was created: {e}")
            raise e


order_service = OrderService(client=bybit_client)
