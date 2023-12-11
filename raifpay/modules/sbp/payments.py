from decimal import Decimal

from raifpay.models.sbp.payments import RaifPayRefund, RaifPayPaymentInfo
from raifpay.modules.module import RaifPayModule


class RaifPaySbpPayments(RaifPayModule):
    async def refund(
        self,
        order_id: str,
        refund_id: str,
        amount: int | float | Decimal,
        statement_description: str | None = None,
        customer_alias: str | None = None,
        customer_phone: str | None = None,
    ) -> RaifPayRefund:
        data = {
            "amount": float(amount),
        }

        if statement_description is not None:
            data["paymentDetails"] = statement_description

        if customer_alias is not None:
            data["customer"]["bankAlias"] = customer_alias
            data["customer"]["phone"] = customer_phone

        return await self.core.request(
            "POST",
            f"/payments/v2/orders/{order_id}/refunds/{refund_id}",
            json=data,
        )

    async def get_refund_info(
        self,
        order_id: str,
        refund_id: str,
    ) -> RaifPayRefund:
        return await self.core.request(
            "GET",
            f"/payments/v2/orders/{order_id}/refunds/{refund_id}",
        )

    async def get_info(self, qr_id: str) -> RaifPayPaymentInfo:
        return await self.core.request(
            "GET",
            f"/sbp/v1/qr/{qr_id}/payment-info",
        )
