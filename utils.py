from decimal import Decimal


def tr_num(v, decimals=2):
    """Türkçe sayı formatı: 12.345,67"""
    s = f"{v:,.{decimals}f}".replace(",", "T").replace(".", ",").replace("T", ".")
    if decimals > 0:
        s = s.rstrip("0")
    if s.endswith(","):
        s = s[:-1]
    return s


def parse_prize(text):
    """Ödül metninden Decimal değer çıkar"""
    return Decimal(text.replace("₺", "").replace(".", "").replace(",", ".").strip())
