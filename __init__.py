"""Flat Rate Shipping plugin."""
from vbwd.plugins.base import BasePlugin, PluginMetadata


DEFAULT_CONFIG = {
    "domestic_rate": 5.99,
    "international_rate": 14.99,
    "currency": "EUR",
    "free_shipping_above": 50.00,
    "estimated_days_domestic": 5,
    "estimated_days_international": 14,
    "domestic_countries": ["DE"],
}


class FlatRateShippingPlugin(BasePlugin):
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="shipping-flat-rate",
            version="1.0.0",
            author="VBWD",
            description="Flat rate shipping — fixed domestic and international rates",
            dependencies=[],
        )

    def initialize(self, config=None):
        merged = {**DEFAULT_CONFIG}
        if config:
            merged.update(config)
        super().initialize(merged)

    def get_blueprint(self):
        return None

    def get_url_prefix(self) -> str:
        return ""

    def on_enable(self):
        pass

    def on_disable(self):
        pass
