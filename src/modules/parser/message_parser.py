import re

from modules.models.dto import (
    SignalOrder,
    SignalOrderType,
    SignalMessage,
    TakeProfitSignal,
    EntrySignal,
    BaseSignal,
)


class MessageParser:
    @staticmethod
    def get_signal(message: SignalMessage) -> BaseSignal | None:
        try:
            if "Take-Profit target" in message.text:
                return MessageParser.parse_take_profit_signal(message)
            elif "All entry targets achieved" in message.text:
                return MessageParser.parse_entry_signal(message)
        except Exception as e:
            return None

    @staticmethod
    def parse_signal_order(text: str) -> SignalOrder:
        lines = text.split("\n")
        signal_data = {}
        for line in lines:
            if "Pair:" in line:
                signal_data["pair"] = line.split(": ")[1].replace("/", "")
            elif "Type:" in line:
                signal_data["type"] = SignalOrderType(line.split(": ")[1])
            elif "Entry:" in line:
                signal_data["entry"] = float(line.split(": ")[1])
            elif "Stop:" in line:
                signal_data["stop"] = float(line.split(": ")[1])
            elif "Take Profit" in line:
                if "profits" not in signal_data:
                    signal_data["profits"] = []
                signal_data["profits"].append(float(line.split(": ")[1]))

        return SignalOrder(**signal_data)

    @staticmethod
    def parse_take_profit_signal(message: SignalMessage) -> TakeProfitSignal:
        order = MessageParser.parse_signal_order(message.reply_to_message.text)
        take_profit = TakeProfitSignal(
            order=order, target=MessageParser.__find_target(message.text)
        )
        return take_profit

    @staticmethod
    def parse_entry_signal(message: SignalMessage) -> EntrySignal:
        order = MessageParser.parse_signal_order(message.reply_to_message.text)
        entry = EntrySignal(order=order, price=MessageParser.__find_price(message.text))
        return entry

    @staticmethod
    def __find_target(text):
        pattern = r"Take-Profit target (\d+)"
        match = re.search(pattern, text)
        return match.group(1)

    @staticmethod
    def __find_price(text):
        pattern = r"Average Entry Price: ([\d.]+)"
        match = re.search(pattern, text)
        return match.group(1)
