# vbwd-plugin-shipping-flat-rate

Flat rate shipping provider -- fixed domestic and international rates.

## Structure

```
plugins/shipping_flat_rate/
├── __init__.py                       # FlatRateShippingPlugin(BasePlugin)
├── shipping_flat_rate/               # Source code
│   └── provider.py                   # FlatRateShippingProvider(IShippingProvider)
└── tests/
    └── unit/
        └── test_provider.py
```

## How It Works

Implements `IShippingProvider` from `vbwd.plugins.shipping_interface`. The plugin registers its provider via `register_shipping_providers(registry)` at startup.

The provider:
- Returns a single `ShippingRate` based on whether the destination is domestic or international
- Supports free shipping above a configurable cart total threshold
- Has no carrier API integration -- tracking is entered manually by the admin

### IShippingProvider Interface

| Method | Description |
|--------|-------------|
| `slug` | Returns `"flat-rate"` |
| `name` | Returns `"Flat Rate Shipping"` |
| `calculate_rate(items, address, currency)` | Returns shipping rate(s) based on destination country |
| `create_shipment(order)` | No-op (manual tracking) |
| `get_tracking(tracking_number)` | Returns `status: "unknown"` |

## Development

```bash
# Unit tests
docker compose run --rm test pytest plugins/shipping_flat_rate/tests/unit/ -v
```

## Configuration

Default values in `__init__.py`:

| Key | Default | Description |
|-----|---------|-------------|
| `domestic_rate` | `5.99` | Shipping cost for domestic orders |
| `international_rate` | `14.99` | Shipping cost for international orders |
| `currency` | `"EUR"` | Rate currency |
| `free_shipping_above` | `50.00` | Cart total for free shipping (0 = disabled) |
| `estimated_days_domestic` | `5` | Estimated delivery days (domestic) |
| `estimated_days_international` | `14` | Estimated delivery days (international) |
| `domestic_countries` | `["DE"]` | Country codes treated as domestic |

## Creating a New Shipping Plugin

To create a custom shipping provider (e.g., DHL, UPS), see the [ecommerce developer guide](../../../docs/dev_docs/ecommerce-developer-guide.md#creating-a-shipping-plugin).
