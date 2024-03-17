from abc import ABC

from models.dto import Position, Order


class ExchangeClient(ABC):
    def get_balance(self) -> float:
        pass

    def get_open_positions(self) -> list[Position]:
        pass

    def place_order(self, order: Order) -> Order:
        pass
