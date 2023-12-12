from os import environ

import pytest

from raifpay import RaifPay
from raifpay.modules.core import API_BASE_SANDBOX

API_SECRET = environ.get('RAIF_API_SECRET')

MERCHANT_ID = "MA0000000552"


@pytest.fixture
def client():
    return RaifPay(API_SECRET, base_url=API_BASE_SANDBOX)
