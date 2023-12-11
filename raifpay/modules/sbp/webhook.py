from raifpay.models.base import RaifPayEmptyResponse
from raifpay.modules.module import RaifPayModule


class RaifPaySbpWebhook(RaifPayModule):
    async def set(self, callback_url: str) -> RaifPayEmptyResponse:
        data = {
            "callbackUrl": callback_url,
        }

        return await self.core.request(
            "POST",
            f"/settings/v1/callback",
            json=data,
        )
