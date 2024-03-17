from __future__ import annotations

from abc import abstractmethod, ABC

from loguru import logger

from models.dto import (
    EntrySignal,
    TakeProfitSignal,
    Position,
    BaseSignal,
    Order,
    OrderType,
    OrderCategory,
)
from modules.core.core import ExchangeClient


class OrderStrategy(ABC):
    def __init__(self, signal: BaseSignal, client: ExchangeClient):
        self.client = client
        self.signal = signal
        logger.info(
            f"Created strategy: {type(self).__name__}. Exchange client: {type(self.client).__name__}"
        )

    @abstractmethod
    def create_order(self):
        pass


class EntryStrategy(OrderStrategy):
    balance = None

    def create_order(self):
        if positions := self.__get_open_positions():
            logger.info(
                f"There are open positions: {[position.symbol for position in positions]}"
            )
            return None
        else:
            self.balance = self.client.get_balance()
            self.__place_order()

    def __get_open_positions(self) -> list[Position]:
        return self.client.get_open_positions()

    def __place_order(self):
        order = Order(
            category=OrderCategory.LINEAR,
            pair="1000PEPEUSDT",
            type=OrderType.BUY,
            qty="3",
            take_profit=0.0085703,
            stop_loss=0.0065703,
        )
        self.client.place_order(order)


class TakeProfitStrategy(OrderStrategy):
    def create_order(self):
        print("Take Profit")


__STRATEGIES = {
    EntrySignal: EntryStrategy,
    TakeProfitSignal: TakeProfitStrategy,
}


def get_strategy(signal, client) -> OrderStrategy:
    return __STRATEGIES[type(signal)](signal, client)
