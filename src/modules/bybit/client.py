from pybit.unified_trading import HTTP

from conf.settings import settings
from models.dto import Position, Order
from modules.core.core import ExchangeClient


class ByBitClient(ExchangeClient):
    def __init__(self, base_url, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

        self.session: HTTP = HTTP(
            testnet=False,
            api_key=self.api_key,
            api_secret=self.api_secret,
        )

    def get_open_positions(self) -> list[Position]:
        response = self.session.get_positions(
            category="linear", settleCoin="USDT", openOnly=True
        )
        result = response["result"]["list"]
        if result:
            return [Position(**position) for position in result]

    def get_balance(self) -> float:
        return self.session.get_wallet_balance(accountType="UNIFIED")["result"]["list"][
            0
        ]["totalAvailableBalance"]

    def place_order(self, order: Order) -> Order | None:
        data = {
            "category": order.category.value.lower(),
            "symbol": order.pair,
            "side": self.__covert_type_to_side(order.type),
            "order_type": "MARKET",
            "qty": str(order.qty),
        }
        if order.take_profit:
            data["takeProfit"] = str(order.take_profit)

        if order.stop_loss:
            data["stopLoss"] = str(order.stop_loss)

        return self.session.place_order(**data)

    def set_leverage(self, pair: str, leverage: int):
        self.session.set_leverage(
            symbol=pair,
            buyLeverage=str(leverage),
            sellLeverage=str(leverage),
            category="linear",
        )

    def get_leverage(self, pair: str) -> int:
        response = self.session.get_positions(category="linear", symbol=pair)
        result = response["result"]["list"]
        if result:
            return int(result[0]["leverage"])

    def get_last_price(self, pair: str) -> float:
        response = self.session.get_tickers(category="linear", symbol=pair)
        result = response["result"]["list"]
        if result:
            return float(result[0]["lastPrice"])

    @staticmethod
    def __covert_type_to_side(order_type: str) -> str:
        if order_type == "BUY":
            return "Buy"
        else:
            return "Sell"


bybit_client = ByBitClient(
    settings.bybit_url, settings.bybit_apikey, settings.bybit_secret
)
