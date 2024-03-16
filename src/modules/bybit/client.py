from pybit.unified_trading import HTTP

from conf.settings import settings
from models.dto import Position


class ByBitClient:
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


bybit_client = ByBitClient(
    settings.bybit_url, settings.bybit_apikey, settings.bybit_secret
)
