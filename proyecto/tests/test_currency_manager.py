import pytest
from unittest.mock import patch  # Añade esta línea
from decimal import Decimal

from classes.currency_manager import CurrencyManager
from config.database import Database

@pytest.fixture
def mock_conversion_rates():
    return {
        "USD": {
            "EUR": Decimal("0.9"),
            "JPY": Decimal("110.5")
        },
        "EUR": {
            "USD": Decimal("1.1"),
            "JPY": Decimal("123.0")
        }
    }
    # Conversión de moneda exitosa (USD a EUR)
def test_convert_currency_success(mock_conversion_rates):
    with patch.object(Database, 'conversion_rates', return_value=mock_conversion_rates):
        tasa_conversion, monto_convertido = CurrencyManager.convert_currency(100, "USD", "EUR")
        assert tasa_conversion == Decimal("0.9")
        assert monto_convertido == Decimal("90.00")
    #Conversión de moneda con divisa de origen desconocida.
def test_convert_currency_unknown_origin_currency(mock_conversion_rates):
    with patch.object(Database, 'conversion_rates', return_value=mock_conversion_rates):
        tasa_conversion, monto_convertido = CurrencyManager.convert_currency(100, "GBP", "EUR")
        assert tasa_conversion is None
        assert monto_convertido is None
    # Conversión de moneda con divisa de destino desconocida.
def test_convert_currency_unknown_destination_currency(mock_conversion_rates):
    with patch.object(Database, 'conversion_rates', return_value=mock_conversion_rates):
        tasa_conversion, monto_convertido = CurrencyManager.convert_currency(100, "USD", "CNY")
        assert tasa_conversion is None
        assert monto_convertido is None
    #Conversión de moneda con monto negativo.
def test_convert_currency_negative_amount(mock_conversion_rates):
    with patch.object(Database, 'conversion_rates', return_value=mock_conversion_rates):
        tasa_conversion, monto_convertido = CurrencyManager.convert_currency(-100, "USD", "EUR")
        assert tasa_conversion == Decimal("0.9")
        assert monto_convertido == Decimal("-90.00")
    #Conversión de moneda con monto cero.
def test_convert_currency_zero_amount(mock_conversion_rates):
    with patch.object(Database, 'conversion_rates', return_value=mock_conversion_rates):
        tasa_conversion, monto_convertido = CurrencyManager.convert_currency(0, "USD", "EUR")
        assert tasa_conversion == Decimal("0.9")
        assert monto_convertido == Decimal("0.00")