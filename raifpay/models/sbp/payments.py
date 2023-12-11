from datetime import datetime
from decimal import Decimal
from typing import Literal, Any

from pydantic import BaseModel, Field

from raifpay.models.base import RaifPayBaseResponse


class RefundStatusInfo(BaseModel):
    value: Literal["IN_PROGRESS", "COMPLETED", "DECLINED"]
    date: datetime
    decline_reason: Literal[
        "TIMEOUT",
        "BANK_NOT_SUPPORTED",
        "RECEIVER_ACCOUNT_ERROR",
        "WRONG_RECIPIENT",
        "SYSTEM_ERROR",
        "RECEIVER_ACCOUNT_NOT_ALLOWED",
    ] | None = Field(None, alias="declineReason")


class RaifPayRefund(RaifPayBaseResponse):
    amount: Decimal
    status: RefundStatusInfo


class RaifPayPaymentInfo(RaifPayBaseResponse):
    internal_description: str
    statement_description: str
    amount: Decimal | None = None
    code: str
    created_at: datetime = Field(alias="createDate")
    currency: str = "RUB"
    order_id: str = Field(alias="order_id")
    status: Literal["SUCCESS", "DECLINED", "NO_INFO", "IN_PROGRESS"] = Field(
        alias="paymentStatus"
    )
    qr_id: str = Field(alias="qrId")
    merchant_id: str = Field(alias="sbpMerchantId")
    paid_at: datetime = Field(alias="transactionDate")
    trx_id: int | None = Field(None, alias="transactionId")
    expiration: datetime = Field(alias="qrExpirationDate")
    extra: dict[str, Any] | None = None
