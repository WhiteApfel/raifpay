from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

from raifpay.models.base import RaifPayBaseResponse


class SubscribeQr(BaseModel):
    qr_id: str = Field(alias="id")
    payload: str
    url: str


class RaifPaySubscription(RaifPayBaseResponse):
    subscription_id: str = Field(alias="id")
    bank: str
    created_at: datetime = Field(alias="createDate")
    status: Literal["INACTIVE", "SUBSCRIBED", "UNSUBSCRIBED"]
    qr: SubscribeQr


class RaifPayPull(RaifPayBaseResponse):
    description: str = Field(alias="additionalInfo")
    statement_description: str = Field(alias="paymentDetails")
    amount: Decimal
    currency: str = "RUB"
    order_id: str = Field(alias="order")
    status: Literal["SUCCESS", "DECLINED", "IN_PROGRESS"] = Field(alias="paymentStatus")
    qr_id: str = Field(alias="qrId")
    merchant_id: str = Field(alias="sbpMerchantId")
