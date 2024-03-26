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
    def create_order(self) -> Order | None:
        pass


class EntryStrategy(OrderStrategy):
    balance: float = None

    def create_order(self):
        if positions := self.__get_open_positions():
            msg = f"There are open positions: {[position.symbol for position in positions]}"
            logger.error(msg)
            raise RuntimeError(msg)
        else:
            self.__get_balance()
            self.__set_leverage()
            return self.__place_order()

    def __get_open_positions(self) -> list[Position]:
        return self.client.get_open_positions()

    def __place_order(self):
        order = Order(
            category=OrderCategory.LINEAR,
            pair=self.signal.order.pair,
            type=OrderType.BUY,
            qty=self.__calculate_quantity(),
            take_profit=self.signal.order.profits[self.signal.tp_target - 1],
            stop_loss=self.signal.order.stop,
            leverage=self.signal.order.leverage,
        )
        logger.info(f"Try to place order: {order}")
        self.client.place_order(order)
        return order

    def __calculate_quantity(self) -> float:
        usdt = (self.balance * self.signal.quantity_percent) / 100
        qnt = int(usdt / self.signal.order.entry)
        logger.info(f"Calculated quantity is {qnt}")
        return qnt

    def __get_balance(self):
        logger.info("Check balance...")
        self.balance = float(self.client.get_balance())
        logger.info(f"Available balance: {self.balance}")

    def __set_leverage(self):
        logger.info(f"Try to set leverage:{self.signal.order.leverage}")
        try:
            self.client.set_leverage(self.signal.order.pair, self.signal.order.leverage)
        except Exception as e:
            logger.warning(f"Leverage not modified: {e}")


class TakeProfitStrategy(OrderStrategy):
    def create_order(self):
        print("Take Profit")


__STRATEGIES = {
    EntrySignal: EntryStrategy,
    TakeProfitSignal: TakeProfitStrategy,
}


def get_strategy(signal, client) -> OrderStrategy:
    return __STRATEGIES[type(signal)](signal, client)
