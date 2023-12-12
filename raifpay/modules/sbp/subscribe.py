import uuid
from decimal import Decimal

from raifpay.models.sbp.subscribe import RaifPayPull, RaifPaySubscription
from raifpay.modules.core import filter_chars
from raifpay.modules.module import RaifPayModule


class RaifPaySbpSubscribe(RaifPayModule):
    async def get_info(self, subscription_id: str) -> RaifPaySubscription:
        return await self.core.request(
            "GET",
            f"/sbp/v1/subscriptions/{subscription_id}",
        )

    async def pull(
        self,
        subscription_id: str,
        description: str,
        amount: Decimal | int | float,
        currency: str = "RUB",
        order_id: str | None = None,
        account: str | None = None,
        statement_description: str | None = None,
    ) -> RaifPayPull:
        data = {
            "amount": float(amount),
            "currency": currency,
        }

        if order_id is None:
            order_id = str(uuid.uuid4())
        data["order"] = order_id

        if statement_description is not None:
            data["paymentDetails"] = statement_description[:185]

        if description is not None:
            description = filter_chars(description)[:140]
            data["additionalInfo"] = description

        if account is not None:
            data["account"] = account

        return await self.core.request(
            "POST",
            f"/sbp/v1/subscriptions/{subscription_id}/orders",
            json=data,
        )

    async def get_pull_info(self, subscription_id: str, order_id: str) -> RaifPayPull:
        return await self.core.request(
            "GET",
            f"/sbp/v1/subscriptions/{subscription_id}/orders/{order_id}",
        )
