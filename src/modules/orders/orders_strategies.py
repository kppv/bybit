from __future__ import annotations

from abc import abstractmethod, ABC

from loguru import logger

from models.dto import EntrySignal, TakeProfitSignal, Position, BaseSignal
from modules.core.core import ExchangeClient


class OrderStrategy(ABC):
    def __init__(self, signal: BaseSignal, client: ExchangeClient):
        self.client = client
        logger.info(
            f"Created strategy: {type(self).__name__}. Exchange client: {type(self.client).__name__}"
        )

    @abstractmethod
    def create_order(self):
        pass


class EntryStrategy(OrderStrategy):
    def create_order(self):
        if positions := self.__get_open_positions():
            logger.info(
                f"There are open positions: {[position.symbol for position in positions]}"
            )

    def __get_open_positions(self) -> list[Position]:
        return self.client.get_open_positions()


class TakeProfitStrategy(OrderStrategy):
    def create_order(self):
        print("Take Profit")


__STRATEGIES = {
    EntrySignal: EntryStrategy,
    TakeProfitSignal: TakeProfitStrategy,
}


def get_strategy(signal, client) -> OrderStrategy:
    return __STRATEGIES[type(signal)](signal, client)
