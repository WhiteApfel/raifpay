from raifpay import RaifPay
from raifpay.models.base import RaifPayEmptyResponse
from raifpay.models.sbp.banks import RaifPayBanks
from raifpay.models.sbp.qr import RaifPayTestQr
from raifpay.modules.module import RaifPayModule
from raifpay.modules.sbp.payments import RaifPaySbpPayments
from raifpay.modules.sbp.qr import RaifPaySbpQr
from raifpay.modules.sbp.subscribe import RaifPaySbpSubscribe
from raifpay.modules.sbp.variable import RaifPaySbpVariable
from raifpay.modules.sbp.webhook import RaifPaySbpWebhook


class RaifPaySbp(RaifPayModule):
    def __init__(self, core: RaifPay):
        super().__init__(core)

        self.qr = RaifPaySbpQr(core)
        self.payments = RaifPaySbpPayments(core)
        self.subscribe = RaifPaySbpSubscribe(core)
        self.variable = RaifPaySbpVariable(core)
        self.webhook = RaifPaySbpWebhook(core)

    async def get_banks(self) -> RaifPayBanks:
        return await self.core.request(
            "GET",
            "/payments/v2/banks",
        )

    async def get_test_info(self, qr_id: str) -> RaifPayTestQr:
        return await self.core.request(
            "GET", f"https://pay-test.raif.ru/api/external-mock/v01/rfuture/qrs/{qr_id}"
        )

    async def test_pay(
        self, qr_id: str, amount: int | float | None = None
    ) -> RaifPayEmptyResponse:
        data = {
            "qrId": qr_id,
        }

        if amount is not None:
            data["amount"] = float(amount)

        return await self.core.request(
            "POST",
            "https://pay-test.raif.ru/api/external-mock/v01/rfuture/payment/init",
            json=data,
        )
