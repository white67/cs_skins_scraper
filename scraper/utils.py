def convert_currency_str_to_symbol(currency_str):
    """
    Convert a currency string to its symbol.

    Args:
        currency_str (str): The currency string to convert.

    Returns:
        str: The corresponding currency symbol.
    """
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "AUD": "A$",
        "CAD": "C$",
        "CHF": "Fr.",
        "CNY": "¥",
        "SEK": "kr",
        "NZD": "$",
        "PLN": "zł",
    }
    return currency_symbols.get(currency_str, currency_str)