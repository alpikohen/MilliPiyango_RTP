import math
from decimal import Decimal

from utils import parse_prize


TOTAL_NUMBERS = 60
SELECTED_NUMBERS = 6
TICKET_PRICE = 25


def calculate_combinations(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))


def calculate_probability(matched=0):
    p = (
        calculate_combinations(SELECTED_NUMBERS, matched)
        * calculate_combinations(TOTAL_NUMBERS - SELECTED_NUMBERS, SELECTED_NUMBERS - matched)
        / calculate_combinations(TOTAL_NUMBERS, SELECTED_NUMBERS)
    )
    if p > 0:
        odds = 1 / p
        odds_str = f"1/{int(odds)}" if odds == int(odds) else f"1/{odds:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    else:
        odds_str = "İmkansız"
    return {"probability": p, "odds": odds_str}


def calculate_rtp(data):
    if not data:
        return None

    total_combinations = calculate_combinations(TOTAL_NUMBERS, SELECTED_NUMBERS)
    category_analysis = {
        i: {"prize_per_winner": 0, "probability": 0, "rtp_percentage": 0, "return_per_25tl": 0}
        for i in range(7)
    }
    total_return = 0.0
    scraped_total_prizes = 0.0
    devir = Decimal("0")

    for section in data:
        for item in section["items"]:
            tunus = int(item["tunus_sayisi"]) if item["tunus_sayisi"].isdigit() else 0
            prize = parse_prize(item["odul_text"])
            kazanan_raw = item["kazanan_sayisi"].strip()
            kazanan_sayisi = 1 if kazanan_raw.lower() == "devir" else (int(kazanan_raw) if kazanan_raw.isdigit() else 0)
            scraped_total_prizes += float(prize) * kazanan_sayisi
            prob = calculate_probability(tunus)["probability"]
            ev = float(prize) * prob
            rtp_pct = (ev / TICKET_PRICE) * 100

            if float(prize) > 1000 and tunus >= 5:
                devir = max(devir, prize)

            category_analysis[tunus] = {
                "prize_per_winner": float(prize),
                "probability": prob,
                "rtp_percentage": rtp_pct,
                "return_per_25tl": ev,
            }
            total_return += ev

    total_prizes = Decimal(str(total_return * total_combinations)) + devir
    rtp_ratio = float(total_prizes / (total_combinations * TICKET_PRICE))

    non_zero_cats = [cat for cat in category_analysis.values() if cat["prize_per_winner"] > 0]
    category_rtp_total = sum(cat["rtp_percentage"] for cat in non_zero_cats)

    return {
        "total_combinations": total_combinations,
        "total_prizes": float(total_prizes),
        "scraped_total_prizes": scraped_total_prizes + float(devir),
        "devir_amount": float(devir),
        "rtp_percentage": rtp_ratio * 100,
        "category_rtp_total": category_rtp_total,
        "return_per_25tl": float(total_return),
        "ticket_price": TICKET_PRICE,
        "category_analysis": category_analysis,
    }
