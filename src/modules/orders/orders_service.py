from modules.models.dto import BaseSignal
from modules.orders.orders_strategies import OrderStrategy


class OrderService:
    def make_order_by_signal(self, signal: BaseSignal):
        if strategy := OrderStrategy.get_strategy_by_signal(signal):
            strategy.create_order()
