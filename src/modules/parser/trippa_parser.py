import re

from loguru import logger

from conf.settings import settings
from models.dto import (
    OrderData,
    OrderType,
    SignalMessage,
    TakeProfitSignal,
    EntrySignal,
    BaseSignal,
)
from modules.parser.message_parser import MessageParser


class TrippaMessageParser(MessageParser):
    def get_signal(self, message: SignalMessage) -> BaseSignal | None:
        try:
            if "Take-Profit target" in message.text:
                return self._parse_take_profit_signal(message)
            elif any(
                keyword.lower() in message.text.lower()
                for keyword in ("all entry targets achieved", "start")
            ):
                return self._parse_entry_signal(message)
        except Exception as e:
            logger.error(f"Error while parsing message: {e}")
            return None

    def _parse_order_data(self, text: str) -> OrderData:
        lines = text.split("\n")
        signal_data = {}
        for line in lines:
            if "Pair:" in line:
                signal_data["pair"] = line.split(":")[1].strip().replace("/", "")
            elif "Type:" in line:
                signal_data["type"] = OrderType(line.split(":")[1].strip())
            elif "Leverage:" in line:
                signal_data["leverage"] = line.split(":")[1].strip().replace("x", "")
            elif "Entry:" in line:
                signal_data["entry"] = float(line.split(":")[1].strip())
            elif "Stop:" in line:
                signal_data["stop"] = float(line.split(":")[1].strip())
            elif "Take Profit" in line:
                if "profits" not in signal_data:
                    signal_data["profits"] = []
                signal_data["profits"].append(float(line.split(":")[1].strip()))

        return OrderData(**signal_data)

    def _parse_take_profit_signal(self, message: SignalMessage) -> TakeProfitSignal:
        order = self._parse_order_data(message.reply_to_message.text)
        take_profit = TakeProfitSignal(
            order=order, target=self.__find_target(message.text)
        )
        return take_profit

    def _parse_entry_signal(self, message: SignalMessage) -> EntrySignal:
        order = self._parse_order_data(message.reply_to_message.text)
        entry = EntrySignal(
            tp_target=self.__find_target(message.text),
            order=order,
            price=self.__find_price(message.text),
            quantity_percent=self.__find_quantity(message.text),
        )
        return entry

    @staticmethod
    def __find_target(text):
        patterns = [r"Take-Profit target (\d+)", r"start (\d+)"]
        for pattern in patterns:
            if match := re.search(pattern, text, re.IGNORECASE):
                return match.group(1)
        return 2

    @staticmethod
    def __find_price(text):
        try:
            pattern = r"Average Entry Price: ([\d.]+)"
            match = re.search(pattern, text, re.IGNORECASE)
            return match.group(1)
        except Exception as e:
            return 0

    @staticmethod
    def __find_quantity(text):
        pattern = r"start (\d+) (\d+)"
        if match := re.search(pattern, text, re.IGNORECASE):
            return match.group(2)
        return settings.default_quantity_percent


trippa_message_parser = TrippaMessageParser()
