from contextvars import ContextVar
from typing import Any, Literal

from httpx import AsyncClient
from httpx import Response as HttpxResponse

context_api_secret: ContextVar[str | None] = ContextVar(
    "context_api_secret", default=None
)

API_BASE_PRODUCTION: str = "https://pay.raif.ru/api"
API_BASE_SANDBOX: str = "https://pay-test.raif.ru/api"

# • Символы латинского алфавита (A–Z и a–z) с десятичными кодами из диапазонов
#   [065-090] и [097-122] в кодировке UTF-8;
# • Символы русского алфавита (А-Я и а-я) с десятичными кодами из диапазона
#   [1040-1103] в кодировке UTF-8;
# • Цифры 0-9 с десятичными кодами из диапазона [048-057] в кодировке UTF-8;
# • Специальные символы с десятичными кодами из диапазонов
#   [032-047], [058-064], [091-096], [123-126] в кодировке UTF-8;
#   - Символ «№» под номером 8470 в кодировке UTF-8
allowed_chars = set(
    list(range(65, 91))
    + list(range(97, 123))
    + list(range(1040, 1104))
    + list(range(48, 58))
    + list(range(32, 48))
    + list(range(58, 65))
    + list(range(91, 97))
    + list(range(123, 127))
    + [8470]
)


def filter_chars(original: str) -> str:
    return "".join([char for char in original if ord(char) in allowed_chars])


class RaifPay:
    def __init__(
        self, api_secret: str | None = None, base_url: str = API_BASE_PRODUCTION
    ):
        self._default_api_secret: str | None = api_secret
        self._http_session: AsyncClient | None = None
        self._base_url: str = base_url

        from raifpay.modules.sbp.core import RaifPaySbp

        self.sbp = RaifPaySbp(self)

    @property
    def http_session(self) -> AsyncClient:
        if self._http_session is None:
            self._http_session = AsyncClient()
        return self._http_session

    async def request(
        self,
        method: Literal["GET", "POST", "DELETE"],
        url: str,
        *,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | float = 5,
        api_secret: str | None = None,
    ) -> HttpxResponse:
        if not url.startswith("https://"):
            url = f"{self._base_url}{url}"

        if api_secret is not None:
            api_secret = api_secret
        elif context_api_secret.get() is not None:
            api_secret = context_api_secret.get()
        elif self._default_api_secret is not None:
            api_secret = self._default_api_secret
        else:
            raise ValueError(
                "TODO: сообщение о том, что надо указать api_secret при вызове метода, "
                "либо в контекст варе, либо при инициализации"
            )

        headers: dict[str, Any] = (headers or {}) | {
            "Authorization": f"Bearer {api_secret}"
        }

        return await self.http_session.request(
            method,
            url,
            json=json,
            params=params,
            headers=headers,
            timeout=timeout,
        )
