import re

from conf.settings import settings
from models.dto import (
    SignalOrder,
    OrderType,
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
            elif any(
                keyword.lower() in message.text.lower()
                for keyword in ("all entry targets achieved", "start")
            ):
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
                signal_data["type"] = OrderType(line.split(": ")[1])
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
        entry = EntrySignal(
            tp_target=MessageParser.__find_target(message.text),
            order=order,
            price=MessageParser.__find_price(message.text),
            quantity_percent=MessageParser.__find_quantity(message.text),
        )
        return entry

    @staticmethod
    def __find_target(text):
        patterns = [r"Take-Profit target (\d+)", r"start (\d+)"]
        for pattern in patterns:
            if match := re.search(pattern, text):
                return match.group(1)
        return 1

    @staticmethod
    def __find_price(text):
        try:
            pattern = r"Average Entry Price: ([\d.]+)"
            match = re.search(pattern, text)
            return match.group(1)
        except Exception as e:
            return 0

    @staticmethod
    def __find_quantity(text):
        pattern = r"start (\d+) (\d+)"
        if match := re.search(pattern, text):
            return match.group(2)
        return settings.default_quantity_percent


message_parser = MessageParser()
