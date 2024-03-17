from models.dto import EntrySignal, SignalOrder, OrderType, TakeProfitSignal
from modules.orders.orders_strategies import (
    get_strategy,
    EntryStrategy,
    TakeProfitStrategy,
)


def test_strategy_is_entry():
    signal = EntrySignal(
        price=0.7031,
        tp_target=1,
        quantity_percent=10,
        order=SignalOrder(
            pair="GALAUSDT",
            type=OrderType.BUY,
            entry=0.0459,
            stop=0.042228,
            profits=[0.046818, 0.047736, 0.049572, 0.051408],
        ),
    )

    strategy = get_strategy(signal, None)

    assert type(strategy) is EntryStrategy


def test_strategy_is_take_profit():
    signal = TakeProfitSignal(
        target=100,
        order=SignalOrder(
            pair="GALAUSDT",
            type=OrderType.BUY,
            entry=0.0459,
            stop=0.042228,
            profits=[0.046818, 0.047736, 0.049572, 0.051408],
        ),
    )

    strategy = get_strategy(signal, None)

    assert type(strategy) is TakeProfitStrategy
