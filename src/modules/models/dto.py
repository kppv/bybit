from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict


class SignalMessage(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    reply_to_message: SignalMessage | None = None


class SignalOrderType(str, Enum):
    BUY = ("BUY",)
    SELL = ("SELL",)


class SignalOrder(BaseModel):
    pair: str
    type: SignalOrderType
    entry: float
    profits: list[float]
    stop: float


class BaseSignal(BaseModel):
    order: SignalOrder


class EntrySignal(BaseSignal):
    price: float


class TakeProfitSignal(BaseSignal):
    target: int
