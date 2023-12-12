import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Literal

from raifpay.models.base import RaifPayEmptyResponse
from raifpay.models.sbp.qr import RaifPayQr
from raifpay.modules.core import filter_chars
from raifpay.modules.module import RaifPayModule


class RaifPaySbpQr(RaifPayModule):
    async def create(
        self,
        merchant_id: str,
        # Global info
        qr_type: Literal["Dynamic", "Static", "Variable"] = "Static",
        description: str | None = None,
        amount: int | float | Decimal | None = None,
        currency: str = "RUB",
        expiration: datetime | timedelta | str | int = 60 * 24 * 3,
        redirect_url: str | None = None,
        # Subscription
        subscription_id: str | bool | None = None,
        subscription_description: str | None = None,
        # Internal info
        order_id: str | None = None,
        internal_description: str | None = None,
        statement_description: str | None = None,
        account: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> RaifPayQr:
        if extra is None:
            extra = {"apiClient": "RaifPay by WhiteApfel", "apiClientVersion": "python"}

        data = {
            "qrType": f"QR{qr_type}",
            "sbpMerchantId": merchant_id,
        }

        if redirect_url is not None:
            data["redirectUrl"] = redirect_url

        if internal_description is not None:
            data["qrDescription"] = internal_description[:32]

        if account is not None:
            data["account"] = account

        if qr_type in ["Static", "Dynamic"]:
            if description is not None:
                description = filter_chars(description)[:140]
                data["additionalInfo"] = description

            if order_id is None:
                order_id = str(uuid.uuid4())
            data["order"] = order_id

            if amount is not None:
                data["amount"] = float(amount)
                data["currency"] = currency

            if statement_description is not None:
                data["paymentDetails"] = statement_description[:185]

            if extra is not None:
                data["extra"] = extra

            if qr_type == "Dynamic":
                if expiration is not None:
                    if isinstance(expiration, int):
                        expiration = timedelta(minutes=expiration)
                    if isinstance(expiration, timedelta):
                        expiration = datetime.now().astimezone() + expiration
                    if isinstance(expiration, datetime):
                        expiration = expiration.astimezone().strftime(
                            "%Y-%m-%dT%H:%M:%S%z"
                        )
                    data["qrExpirationDate"] = str(expiration)

                if subscription_id is not None:
                    data["subscription"] = {}
                    if subscription_id is True:
                        subscription_id = str(uuid.uuid4())
                    data["subscription"]["id"] = subscription_id

                    if subscription_description is None:
                        subscription_description = f"Подписка в магазине #{merchant_id}"
                    data["subscription"]["subscriptionPurpose"] = (
                        subscription_description[:140]
                    )

        return await self.core.request("POST", "/sbp/v2/qrs", json=data)

    async def get_info(self, qr_id: str) -> RaifPayQr:
        return await self.core.request("GET", f"/sbp/v2/qrs/{qr_id}")

    async def cancel(self, qr_id: str) -> RaifPayEmptyResponse:
        return await self.core.request("DELETE", f"/sbp/v2/qrs/{qr_id}")
