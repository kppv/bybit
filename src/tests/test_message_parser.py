from messages_data import *
from models.dto import (
    OrderType,
    SignalMessage,
    TakeProfitSignal,
)
from modules.messages.parsers import MessageParser

MSG = """
👉 Pair: KAVA/USDT
👉 Type: BUY
👉 Leverage: 20x
👉 Entry: 0.9717

❌ Stop: 0.893964

✅ Take Profit 1: 0.991134
✅ Take Profit 2: 1.010568
✅ Take Profit 3: 1.049436
✅ Take Profit 4: 1.088304
"""


def test_parse_signal_order():
    signal = MessageParser.parse_signal_order(MSG)
    assert signal.pair == "KAVAUSDT"
    assert signal.type == OrderType.BUY
    assert signal.entry == 0.9717
    assert signal.stop == 0.893964
    assert signal.profits == [0.991134, 1.010568, 1.049436, 1.088304]
    assert signal.leverage == 20


def test_parse_take_profit_signal():
    take_profit = MessageParser.parse_take_profit_signal(
        SignalMessage(**TAKE_PROFIT_MESSAGE)
    )
    assert take_profit.order.pair == "GALAUSDT"
    assert take_profit.order.type == OrderType.BUY
    assert take_profit.order.entry == 0.0459
    assert take_profit.order.stop == 0.042228
    assert take_profit.order.profits == [0.046818, 0.047736, 0.049572, 0.051408]
    assert take_profit.target == 2


def test_parse_entry_signal():
    entry = MessageParser.parse_entry_signal(SignalMessage(**ENTRY_SIGNAL_MESSAGE))
    assert entry.order.pair == "GALAUSDT"
    assert entry.order.type == OrderType.BUY
    assert entry.order.entry == 0.0459
    assert entry.order.stop == 0.042228
    assert entry.order.profits == [0.046818, 0.047736, 0.049572, 0.051408]
    assert entry.price == 0.7031


def test_parse_custom_entry_signal():
    msg = ENTRY_SIGNAL_MESSAGE.copy()
    msg["text"] = "start 3 54"
    entry = MessageParser.parse_entry_signal(SignalMessage(**msg))
    assert entry.order.pair == "GALAUSDT"
    assert entry.order.type == OrderType.BUY
    assert entry.order.entry == 0.0459
    assert entry.order.stop == 0.042228
    assert entry.order.profits == [0.046818, 0.047736, 0.049572, 0.051408]
    assert entry.price == 0
    assert entry.tp_target == 3
    assert entry.quantity_percent == 54


def test_parse_custom_entry_signal_upper_case():
    msg = ENTRY_SIGNAL_MESSAGE.copy()
    msg["text"] = "STart 3 54"
    entry = MessageParser.parse_entry_signal(SignalMessage(**msg))
    assert entry.order.pair == "GALAUSDT"
    assert entry.order.type == OrderType.BUY
    assert entry.order.entry == 0.0459
    assert entry.order.stop == 0.042228
    assert entry.order.profits == [0.046818, 0.047736, 0.049572, 0.051408]
    assert entry.price == 0
    assert entry.tp_target == 3
    assert entry.quantity_percent == 54


def test_message_is_take_profit_signal():
    signal = MessageParser.get_signal(SignalMessage(**TAKE_PROFIT_MESSAGE))
    assert type(signal) is TakeProfitSignal


def test_other_message():
    signal = MessageParser.get_signal(
        SignalMessage(**{"id": 1, "text": "Some other message \n with \n new lines"})
    )
    assert signal is None
