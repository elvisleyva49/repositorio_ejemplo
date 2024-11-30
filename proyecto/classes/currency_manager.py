from decimal import Decimal, ROUND_HALF_UP
from config.database import Database

class CurrencyManager:
    @staticmethod
    def convert_currency(monto, divisa_origen, divisa_destino):
        conversion_rates = Database.conversion_rates()
        
        if divisa_origen in conversion_rates and divisa_destino in conversion_rates[divisa_origen]:
            tasa_conversion = Decimal(conversion_rates[divisa_origen][divisa_destino]).quantize(
                Decimal('0.0001'), rounding=ROUND_HALF_UP)
            monto_decimal = Decimal(str(monto)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            monto_convertido = (monto_decimal * tasa_conversion).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP)
            return tasa_conversion, monto_convertido
        return None, None
    