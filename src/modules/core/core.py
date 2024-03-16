from typing import Protocol

from models.dto import Position


class ExchangeClient(Protocol):
    def get_open_positions(self) -> list[Position]:
        pass
