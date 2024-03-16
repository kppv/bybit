from loguru import logger

from models.dto import BaseSignal
from modules.bybit.client import bybit_client
from modules.core.core import ExchangeClient
from modules.orders.orders_strategies import get_strategy


class OrderService:
    def __init__(self, client: ExchangeClient):
        self.client = client

    def make_order_by_signal(self, signal: BaseSignal):
        strategy = get_strategy(signal, self.client)
        strategy.create_order()


order_service = OrderService(client=bybit_client)
