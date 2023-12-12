import pytest

from tests.conftest import MERCHANT_ID


@pytest.fixture
async def static_qr(client):
    return await client.sbp.qr.create(
        merchant_id=MERCHANT_ID,
        qr_type="Static",
        description="Test static qr",
    )


@pytest.fixture
async def static_qr_with_amount(client):
    return await client.sbp.qr.create(
        merchant_id=MERCHANT_ID,
        qr_type="Static",
        description="Test static qr with amount",
        amount=150,
    )


@pytest.fixture
async def dynamic_qr(client):
    return await client.sbp.qr.create(
        merchant_id=MERCHANT_ID,
        qr_type="Dynamic",
        description="Test dynamic qr",
        amount=150,
    )


@pytest.fixture
async def dynamic_qr_with_subscription(client):
    return await client.sbp.qr.create(
        merchant_id=MERCHANT_ID,
        qr_type="Dynamic",
        description="Test dynamic qr with subscription",
        amount=150,
        subscription_id=True,
        subscription_description="Test subscription",
    )


@pytest.fixture
async def variable_qr(client):
    return await client.sbp.qr.create(
        merchant_id=MERCHANT_ID,
        qr_type="Variable",
    )
