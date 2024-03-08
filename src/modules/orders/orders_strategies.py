from __future__ import annotations

from abc import abstractmethod

from models.dto import SignalOrder, EntrySignal, TakeProfitSignal


class OrderStrategy:
    @abstractmethod
    def create_order(self, signal: SignalOrder = None):
        pass


class EntryStrategy(OrderStrategy):
    def create_order(self, signal: SignalOrder = None):
        print("ENTER")


class TakeProfitStrategy(OrderStrategy):
    def create_order(self, signal: SignalOrder = None):
        print("Take Profit")


__STRATEGIES = {
    EntrySignal: EntryStrategy,
    TakeProfitSignal: TakeProfitStrategy,
}


def get_strategy_by_signal(signal):
    return __STRATEGIES[type(signal)]()
