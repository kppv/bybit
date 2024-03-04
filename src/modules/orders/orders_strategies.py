from __future__ import annotations

from abc import abstractmethod

from modules.models.dto import SignalOrder, BaseSignal, EntrySignal, TakeProfitSignal


class OrderStrategy:
    @abstractmethod
    def create_order(self, signal: SignalOrder = None):
        pass

    @staticmethod
    def get_strategy_by_signal(signal: BaseSignal) -> OrderStrategy | None:
        if type(signal) is EntrySignal:
            return EntryStrategy()
        elif type(signal) is TakeProfitSignal:
            return TakeProfitStrategy()
        else:
            return None


class EntryStrategy(OrderStrategy):
    def create_order(self, signal: SignalOrder = None):
        print("ENTER")


class TakeProfitStrategy(OrderStrategy):
    def create_order(self, signal: SignalOrder = None):
        print("Take Profit")
