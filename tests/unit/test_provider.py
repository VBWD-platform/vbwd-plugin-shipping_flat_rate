"""Unit tests for FlatRateShippingProvider — Sprint 06f."""
from decimal import Decimal

import pytest

from plugins.shipping_flat_rate.shipping_flat_rate.provider import (
    FlatRateShippingProvider,
)


@pytest.fixture()
def config():
    return {
        "domestic_rate": 5.99,
        "international_rate": 14.99,
        "free_shipping_above": 50.00,
        "estimated_days_domestic": 5,
        "estimated_days_international": 14,
        "domestic_countries": ["DE"],
    }


@pytest.fixture()
def provider(config):
    return FlatRateShippingProvider(config)


class TestSlugAndName:
    def test_slug(self, provider):
        assert provider.slug == "flat-rate"

    def test_name(self, provider):
        assert provider.name == "Flat Rate Shipping"


class TestCalculateRate:
    def test_domestic_rate(self, provider):
        rates = provider.calculate_rate(
            items=[{"total_price": 30}],
            address={"country": "DE"},
            currency="EUR",
        )
        assert len(rates) == 1
        assert rates[0].cost == Decimal("5.99")
        assert rates[0].estimated_days == 5

    def test_international_rate(self, provider):
        rates = provider.calculate_rate(
            items=[{"total_price": 30}],
            address={"country": "US"},
            currency="EUR",
        )
        assert len(rates) == 1
        assert rates[0].cost == Decimal("14.99")
        assert rates[0].estimated_days == 14

    def test_free_shipping_above_threshold(self, provider):
        rates = provider.calculate_rate(
            items=[{"total_price": 60}],
            address={"country": "DE"},
            currency="EUR",
        )
        assert len(rates) == 1
        assert rates[0].cost == Decimal("0.00")
        assert "Free" in rates[0].name

    def test_no_free_shipping_below_threshold(self, provider):
        rates = provider.calculate_rate(
            items=[{"total_price": 40}],
            address={"country": "DE"},
            currency="EUR",
        )
        assert rates[0].cost > 0

    def test_free_shipping_disabled_when_zero(self, config):
        config["free_shipping_above"] = 0
        provider = FlatRateShippingProvider(config)
        rates = provider.calculate_rate(
            items=[{"total_price": 1000}],
            address={"country": "DE"},
            currency="EUR",
        )
        assert rates[0].cost == Decimal("5.99")
