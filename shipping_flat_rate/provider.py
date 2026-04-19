"""Flat rate shipping provider."""
from decimal import Decimal
from typing import Any, Dict, List

from vbwd.plugins.shipping_interface import (
    IShippingProvider,
    ShippingRate,
    ShipmentResult,
    TrackingInfo,
)


class FlatRateShippingProvider(IShippingProvider):
    """Simple flat-rate shipping — fixed price for domestic and international."""

    def __init__(self, config: Dict[str, Any]):
        self._config = config

    @property
    def slug(self) -> str:
        return "flat-rate"

    @property
    def name(self) -> str:
        return "Flat Rate Shipping"

    def calculate_rate(
        self, items: List[Dict[str, Any]], address: Dict[str, Any], currency: str
    ) -> List[ShippingRate]:
        country = (address.get("country") or "").upper()
        domestic_countries = self._config.get("domestic_countries", ["DE"])
        is_domestic = country in domestic_countries

        # Check free shipping threshold
        cart_total = sum(
            Decimal(str(item.get("total_price", 0))) for item in items
        )
        free_above = Decimal(str(self._config.get("free_shipping_above", 0)))
        if free_above > 0 and cart_total >= free_above:
            return [
                ShippingRate(
                    provider_slug=self.slug,
                    name="Free Shipping",
                    cost=Decimal("0.00"),
                    currency=currency,
                    estimated_days=self._config.get("estimated_days_domestic", 5)
                    if is_domestic
                    else self._config.get("estimated_days_international", 14),
                    description="Free shipping on orders above threshold",
                )
            ]

        if is_domestic:
            rate = Decimal(str(self._config.get("domestic_rate", "5.99")))
            days = self._config.get("estimated_days_domestic", 5)
            label = "Standard Domestic Shipping"
        else:
            rate = Decimal(str(self._config.get("international_rate", "14.99")))
            days = self._config.get("estimated_days_international", 14)
            label = "International Shipping"

        return [
            ShippingRate(
                provider_slug=self.slug,
                name=label,
                cost=rate,
                currency=currency,
                estimated_days=days,
            )
        ]

    def create_shipment(self, order: Dict[str, Any]) -> ShipmentResult:
        # Flat rate has no carrier integration — manual tracking
        return ShipmentResult(success=True, tracking_number="", tracking_url="")

    def get_tracking(self, tracking_number: str) -> TrackingInfo:
        return TrackingInfo(status="unknown")
