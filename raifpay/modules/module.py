import inspect
from types import GenericAlias

import ujson
from httpx import Response

from raifpay.errors.base import RaifPayError
from raifpay.models.base import (
    RaifPayBaseResponse,
    RaifPayEmptyResponse,
    RaifPayRootResponse,
)
from raifpay.modules.core import RaifPay, context_api_secret


class RaifPayModule:
    def __new__(cls, *args, **kwargs):
        for name, function in inspect.getmembers(cls, predicate=inspect.isfunction):
            if name.startswith("__"):
                continue
            if (
                "return" in function.__annotations__
                and isinstance(function.__annotations__["return"], type)
                and not isinstance(function.__annotations__["return"], GenericAlias)
                and (
                    issubclass(function.__annotations__["return"], RaifPayBaseResponse)
                    or issubclass(
                        function.__annotations__["return"], RaifPayRootResponse
                    )
                )
            ):

                def decorate(f):
                    async def decorated(*f_args, **f_kwargs):
                        token = None
                        if f_kwargs.get("api_secret") is not None:
                            token = context_api_secret.set(f_kwargs.get("api_secret"))
                        if (
                            "api_secret" not in inspect.getfullargspec(f).args
                            and "api_secret" in f_kwargs
                        ):
                            del f_kwargs["api_secret"]
                        response: Response = await f(*f_args, **f_kwargs)

                        if token is not None:
                            context_api_secret.reset(token)

                        if (
                            response.status_code
                            == f.__annotations__["return"]._valid_status_code.default
                        ):
                            if f.__annotations__["return"]._is_empty.default:
                                return RaifPayEmptyResponse()
                            return f.__annotations__["return"].model_validate(
                                ujson.loads(response.text)
                            )
                        else:
                            raise RaifPayError(response)

                    return decorated

                setattr(cls, name, decorate(function))

        return super(RaifPayModule, cls).__new__(cls)  # noqa: UP008

    def __init__(self, core: RaifPay):
        self.core = core
