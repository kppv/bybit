from abc import ABC

from models.dto import (
    OrderData,
    SignalMessage,
    TakeProfitSignal,
    EntrySignal,
    BaseSignal,
)


class MessageParser(ABC):
    def get_signal(self, message: SignalMessage) -> BaseSignal | None:
        pass

    def _parse_order_data(self, text: str) -> OrderData:
        pass

    def _parse_take_profit_signal(self, message: SignalMessage) -> TakeProfitSignal:
        pass

    def _parse_entry_signal(self, message: SignalMessage) -> EntrySignal:
        pass
