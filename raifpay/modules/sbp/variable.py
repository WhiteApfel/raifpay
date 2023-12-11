from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

import uuid

from raifpay.models.base import RaifPayEmptyResponse
from raifpay.models.sbp.qr import RaifPayQr
from raifpay.models.sbp.variable import RaifPayVariableOrder
from raifpay.modules.module import RaifPayModule


class RaifPaySbpVariable(RaifPayModule):
    async def create(
        self,
        qr_id: str,
        amount: Decimal | int | float,
        order_id: str | None = None,
        description: str | None = None,
        expiration: datetime | timedelta | str | int = 15,
        internal_description: str | None = None,
        statement_description: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> RaifPayVariableOrder:
        if extra is None:
            extra = {"apiClient": "RaifPay by WhiteApfel", "apiClientVersion": "python"}

        data = {"amount": amount, "extra": extra, "qr": {"id": qr_id}}

        if order_id is None:
            order_id = str(uuid.uuid4())
        data["order"] = order_id

        if description is not None:
            data["comment"] = description

        if internal_description is not None:
            data["qr"]["additionalInfo"] = internal_description[:140]

        if statement_description is not None:
            data["qr"]["paymentDetails"] = statement_description[:140]

        if internal_description is not None:
            data["qrDescription"] = internal_description[:32]

        if expiration is not None:
            if isinstance(expiration, timedelta):
                expiration = expiration.seconds // 60
            elif isinstance(expiration, datetime):
                expiration = expiration.astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
        data["qrExpirationDate"] = expiration

        return await self.core.request(
            "POST",
            "/payment/v1/orders",
            json=data,
        )

    async def get_info(self, order_id: str) -> RaifPayVariableOrder:
        return await self.core.request(
            "GET",
            f"/payment/v1/orders/{order_id}",
        )

    async def cancel(self, order_id: str) -> RaifPayEmptyResponse:
        return await self.core.request(
            "DELETE",
            f"/payment/v1/orders/{order_id}",
        )

    async def link(
        self,
        qr_id: str,
        account: str,
        redirect_url: str | None = None,
        internal_description: str | None = None,
    ) -> RaifPayQr:
        data = {
            "account": account,
        }

        if redirect_url is not None:
            data["redirectUrl"] = redirect_url

        if internal_description is not None:
            data["qrDescription"] = internal_description[:32]

        return await self.core.request(
            "POST",
            f"/sbp/v1/qr-drafts/{qr_id}",
            json=data,
        )
