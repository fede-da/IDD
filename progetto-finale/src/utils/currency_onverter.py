import re

class CurrencyConverter:
    def __init__(self):
        # Hypothetical conversion rates to USD
        self.conversion_rates = {
            "EUR": 1.1,  # Example: 1 EUR = 1.1 USD
            "GBP": 1.3,  # Example: 1 GBP = 1.3 USD
            "JPY": 0.009,  # Example: 1 JPY = 0.009 USD
        }
        self.currency_symbols = {
            "USD": "$",
            "EUR": "€",
            "GBP": "£",
            "JPY": "¥",
        }

    def RecognizeCurrencyAndConvertToUsd(self, string_to_analyze):
        try:
            # Detect currency and extract numeric value
            currency, value, unit = self._parse_string(string_to_analyze)
            if currency not in self.conversion_rates:
                raise ValueError(f"Unsupported currency: {currency}")
            usd_value = self._convert_to_usd(value, currency)
            return f"${usd_value:.2f} {unit}"
        except Exception as e:
            print(f"Failed conversion: {e}")
            return None

    def FromUsdToCurrency(self, value_in_usd, currency):
        try:
            if currency not in self.conversion_rates:
                raise ValueError(f"Unsupported currency: {currency}")
            converted_value = float(value_in_usd) / self.conversion_rates[currency]
            return f"{self.currency_symbols.get(currency, '$')}{converted_value:.2f}"
        except Exception as e:
            print(f"Failed conversion: {e}")
            return None

    def _convert_to_usd(self, value, currency):
        # Convert value to USD based on the detected currency
        return value * self.conversion_rates.get(currency, 1)  # Default to 1 if USD or not found

    def _parse_string(self, string):
        try:
            # Parse the string to detect currency, value, and unit
            currency_detected = None
            for cur, symbol in self.currency_symbols.items():
                if symbol in string:
                    currency_detected = cur
                    break
            if not currency_detected:
                raise ValueError("Currency symbol not found in string")
            value_str = re.findall(r"\d+\.\d+", string)[0]
            value = float(value_str) if value_str else 0
            unit = re.findall(r"Billion|Million|B|M|T", string, re.IGNORECASE)[0]
            return currency_detected, value, unit
        except Exception as e:
            print(f"Failed to parse string: {e}")
            return None, 0, None

# Example usage
converter = CurrencyConverter()
print(converter.RecognizeCurrencyAndConvertToUsd("€349.50 Billion"))  # Example conversion from EUR to USD
print(converter.FromUsdToCurrency("349.50", "GBP"))  # Example conversion from USD to GBP
