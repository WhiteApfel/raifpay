from typing import Any

from pydantic import BaseModel, RootModel


class RaifPayBaseResponse(BaseModel):
    _valid_status_code: int = 200
    _is_empty: bool = False


class RaifPayEmptyResponse(RaifPayBaseResponse):
    _is_empty: bool = True


class RaifPayRootResponse(RootModel):
    _valid_status_code: int = 200
    root: list[Any]
