from datetime import datetime
from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, Field

from raifpay.models.base import RaifPayBaseResponse


class VariableStatus(BaseModel):
    value: Literal["NEW", "CANCELLED", "EXPIRED", "PAID"]
    date: datetime


class QrInfo(BaseModel):
    qr_id: str = Field(alias="qrId")
    description: str | None = Field(None, alias="additionalInfo")
    statement_description: str | None = Field(None, alias="paymentDetails")


class RaifPayVariableOrder(RaifPayBaseResponse):
    order_id: str
    amount: Decimal
    description: str = Field(alias="comment")
    extra: dict[str, Any] | None = None
    status: VariableStatus
    expiration: datetime = Field(alias="expirationDate")
    qr: QrInfo
