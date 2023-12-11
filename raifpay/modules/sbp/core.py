from raifpay import RaifPay
from raifpay.models.sbp.banks import RaifPayBanks
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
