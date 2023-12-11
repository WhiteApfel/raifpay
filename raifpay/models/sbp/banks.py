from pydantic import BaseModel

from raifpay.models.base import RaifPayRootResponse


class Bank(BaseModel):
    alias: str
    name: str


class RaifPayBanks(RaifPayRootResponse):
    root: list[Bank]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        # TODO: добавить поиск по имени (нечёткий)
        return self.root[item]
