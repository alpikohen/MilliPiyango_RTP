from decimal import Decimal


def tr_num(value, decimals=2):
    """Türkçe sayı formatı: 12.345,67."""
    formatted = f"{value:,.{decimals}f}".replace(",", "T").replace(".", ",").replace("T", ".")
    if decimals > 0:
        formatted = formatted.rstrip("0")
    if formatted.endswith(","):
        formatted = formatted[:-1]
    return formatted


def parse_prize(text):
    """Türkçe para metnini Decimal değere dönüştür."""
    return Decimal(text.replace("₺", "").replace(".", "").replace(",", ".").strip())
