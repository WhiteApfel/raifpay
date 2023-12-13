from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import Field

from raifpay.models.base import RaifPayBaseResponse


class RaifPayQr(RaifPayBaseResponse):
    qr_id: str = Field(alias="qrId")
    status: Literal[
        "NEW", "INACTIVE", "IN_PROGRESS", "PAID", "EXPIRED", "CANCELLED"
    ] = Field(alias="qrStatus")
    payload: str
    url: str = Field(alias="qrUrl")
    expiration: datetime | None = Field(None, alias="qrExpirationDate")
    subscription_id: str | None = Field(None, alias="subscriptionId")


class RaifPayTestQr(RaifPayBaseResponse):
    qrc_type: Literal["01", "02"] = Field(alias="qrcType")
    amount: Decimal | None = Field(None, alias="sum")
    currency: str
    status: Literal["NEW", "INACTIVE", "IN_PROGRESS", "PAID", "EXPIRED", "CANCELLED"]
    redirect_url: str | None = Field(None, alias="redirectUrl")
