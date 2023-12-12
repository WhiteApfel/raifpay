from os import environ

__version__ = environ.get("TAG_VERSION", "dev").replace("v", "")

from raifpay.modules.core import RaifPay
