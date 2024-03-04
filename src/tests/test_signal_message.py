from messages_data import *
from models.dto import SignalMessage


def test_signal_message():
    signal_message = SignalMessage(**MESSAGE)

    assert signal_message.id == MESSAGE["id"]
    assert signal_message.text == MESSAGE["text"]


def test_reply_take_profit_signal_message():
    signal_message = SignalMessage(**TAKE_PROFIT_MESSAGE)

    assert signal_message.id == TAKE_PROFIT_MESSAGE["id"]
    assert signal_message.text == TAKE_PROFIT_MESSAGE["text"]

    assert signal_message.reply_to_message.id == MESSAGE["id"]
    assert signal_message.reply_to_message.text == MESSAGE["text"]
