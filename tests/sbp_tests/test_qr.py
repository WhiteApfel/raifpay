from typing import Awaitable

import pytest

from raifpay import RaifPay
from raifpay.models.sbp.qr import RaifPayQr


@pytest.mark.asyncio
async def test_create_static_qr(static_qr: Awaitable[RaifPayQr]):
    static_qr = await static_qr
    assert static_qr.status == "NEW"
    assert static_qr.subscription_id is None


@pytest.mark.asyncio
async def test_create_static_qr_with_amount(
    static_qr_with_amount: Awaitable[RaifPayQr],
):
    static_qr_with_amount = await static_qr_with_amount
    assert static_qr_with_amount.status == "NEW"
    assert static_qr_with_amount.subscription_id is None


@pytest.mark.asyncio
async def test_create_dynamic_qr(dynamic_qr: Awaitable[RaifPayQr]):
    dynamic_qr = await dynamic_qr
    assert dynamic_qr.status == "NEW"
    assert dynamic_qr.subscription_id is None


@pytest.mark.asyncio
async def test_create_dynamic_qr_with_subscription(
    dynamic_qr_with_subscription: Awaitable[RaifPayQr],
):
    dynamic_qr_with_subscription = await dynamic_qr_with_subscription
    assert dynamic_qr_with_subscription.status == "NEW"
    assert dynamic_qr_with_subscription.subscription_id is not None


@pytest.mark.asyncio
async def test_create_variable_qr(variable_qr: Awaitable[RaifPayQr]):
    variable_qr = await variable_qr
    assert variable_qr.status == "INACTIVE"
    assert variable_qr.subscription_id is None


@pytest.mark.asyncio
async def test_cancel_static_qr(client: RaifPay, static_qr: Awaitable[RaifPayQr]):
    static_qr = await static_qr
    assert static_qr.status == "NEW"
    assert static_qr.subscription_id is None

    await client.sbp.qr.cancel(static_qr.qr_id)

    qr_info = await client.sbp.qr.get_info(static_qr.qr_id)

    assert qr_info.status == "CANCELLED"


@pytest.mark.asyncio
async def test_cancel_dynamic_qr(client: RaifPay, dynamic_qr: Awaitable[RaifPayQr]):
    dynamic_qr = await dynamic_qr
    assert dynamic_qr.status == "NEW"
    assert dynamic_qr.subscription_id is None

    await client.sbp.qr.cancel(dynamic_qr.qr_id)

    qr_info = await client.sbp.qr.get_info(dynamic_qr.qr_id)

    assert qr_info.status == "CANCELLED"

