from __future__ import annotations

from enum import Enum, StrEnum

from pydantic import BaseModel, ConfigDict


class SignalMessage(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    reply_to_message: SignalMessage | None = None


class OrderType(str, Enum):
    BUY = ("BUY",)
    SELL = ("SELL",)


class OrderCategory(StrEnum):
    LINEAR = ("LINEAR",)
    SPOT = ("SPOT",)


class SignalOrder(BaseModel):
    pair: str
    type: OrderType
    entry: float
    profits: list[float]
    stop: float
    leverage: int


class BaseSignal(BaseModel):
    order: SignalOrder


class EntrySignal(BaseSignal):
    price: float
    tp_target: int
    quantity_percent: float


class TakeProfitSignal(BaseSignal):
    target: int


class Position(BaseModel):
    symbol: str | None = None
    leverage: str | None = None
    autoAddMargin: int | None = None
    avgPrice: str | None = None
    liqPrice: str | None = None
    riskLimitValue: str | None = None
    takeProfit: str | None = None
    positionValue: str | None = None
    isReduceOnly: bool | None = None
    tpslMode: str | None = None
    riskId: int | None = None
    trailingStop: str | None = None
    unrealisedPnl: str | None = None
    markPrice: str | None = None
    adlRankIndicator: int | None = None
    cumRealisedPnl: str | None = None
    positionMM: str | None = None
    createdTime: str | None = None
    positionIdx: int | None = None
    positionIM: str | None = None
    seq: int | None = None
    updatedTime: str | None = None
    side: str | None = None
    bustPrice: str | None = None
    positionBalance: str | None = None
    leverageSysUpdatedTime: str | None = None
    curRealisedPnl: str | None = None
    size: str | None = None
    positionStatus: str | None = None
    mmrSysUpdatedTime: str | None = None
    stopLoss: str | None = None
    tradeMode: int | None = None
    sessionAvgPrice: str | None = None


class Order(BaseModel):
    pair: str
    category: OrderCategory
    type: OrderType
    qty: float
    take_profit: float | None = None
    stop_loss: float | None = None
    leverage: float = 1
    last_price: float | None = None
