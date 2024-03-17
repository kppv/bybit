from abc import ABC

from models.dto import Position, Order


class ExchangeClient(ABC):
    def get_balance(self) -> float:
        pass

    def get_open_positions(self) -> list[Position]:
        pass

    def place_order(self, order: Order) -> Order:
        pass

    def enable_cross_margin(self, pair: str):
        pass

    def set_leverage(self, pair: str, leverage: int):
        pass
