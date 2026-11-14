import math
from decimal import Decimal

from lottery_analyzer.games.sans_topu.rules import (
    BONUS_NUMBERS,
    ALL_CATEGORIES,
    DRAWN_NUMBERS,
    SELECTED_NUMBERS,
    TICKET_PRICE,
    TOTAL_NUMBERS,
    WINNING_CATEGORIES,
)
from lottery_analyzer.shared.formatting import parse_prize
from lottery_analyzer.shared.tax_calculator import calculate_tax


def calculate_combinations(n, r):
    return math.comb(n, r) if 0 <= r <= n else 0


def calculate_probability(category):
    category = str(category).strip()
    has_bonus_match = "+" in category
    main_matches = int(category.split("+", maxsplit=1)[0])
    if main_matches < 0 or main_matches > SELECTED_NUMBERS:
        return {"probability": 0, "odds": "İmkansız"}

    main_probability = (
        calculate_combinations(DRAWN_NUMBERS, main_matches)
        * calculate_combinations(
            TOTAL_NUMBERS - DRAWN_NUMBERS,
            SELECTED_NUMBERS - main_matches,
        )
        / calculate_combinations(TOTAL_NUMBERS, SELECTED_NUMBERS)
    )
    bonus_probability = (
        1 / BONUS_NUMBERS
        if has_bonus_match
        else (BONUS_NUMBERS - 1) / BONUS_NUMBERS
    )
    probability = main_probability * bonus_probability
    odds = 1 / probability
    odds_text = (
        f"1/{int(odds)}"
        if odds == int(odds)
        else f"1/{odds:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    )
    return {"probability": probability, "odds": odds_text}


def calculate_rtp(data):
    if not data:
        return None

    total_combinations = calculate_combinations(TOTAL_NUMBERS, SELECTED_NUMBERS) * BONUS_NUMBERS
    category_analysis = {
        category: {
            "label": category,
            "prize_per_winner": 0,
            "probability": calculate_probability(category)["probability"],
            "rtp_percentage": 0,
            "return_per_ticket": 0,
        }
        for category in ALL_CATEGORIES
    }
    total_return = 0.0
    scraped_total_prizes = 0.0
    rollover = Decimal("0")

    for section in data:
        for item in section["items"]:
            category_name = str(item["tutus_sayisi"]).strip().replace(" ", "")
            if category_name not in category_analysis:
                continue

            prize = parse_prize(item["odul_text"])
            winners_text = item["kazanan_sayisi"].strip()
            winner_count = int(winners_text) if winners_text.isdigit() else 0
            scraped_total_prizes += float(prize) * winner_count

            probability = calculate_probability(category_name)["probability"]
            expected_value = (float(prize) - calculate_tax(float(prize))) * probability
            rtp_percentage = (expected_value / TICKET_PRICE) * 100

            if item.get("kazanan_text", "").strip().casefold() == "devir":
                rollover = max(rollover, prize)

            category_analysis[category_name] = {
                "label": category_name,
                "prize_per_winner": float(prize),
                "probability": probability,
                "rtp_percentage": rtp_percentage,
                "return_per_ticket": expected_value,
            }
            total_return += expected_value

    total_prizes = Decimal(str(total_return * total_combinations)) + rollover
    rtp_ratio = float(total_prizes / (total_combinations * TICKET_PRICE))
    non_zero_categories = [
        category for category in category_analysis.values()
        if category["prize_per_winner"] > 0
    ]
    category_rtp_total = sum(
        category["rtp_percentage"] for category in non_zero_categories
    )

    return {
        "total_combinations": total_combinations,
        "combination_formula": "C(34, 5) × 14",
        "total_prizes": float(total_prizes),
        "scraped_total_prizes": scraped_total_prizes + float(rollover),
        "devir_amount": float(rollover),
        "rtp_percentage": rtp_ratio * 100,
        "category_rtp_total": category_rtp_total,
        "return_per_ticket": float(total_return),
        "ticket_price": TICKET_PRICE,
        "category_order": list(ALL_CATEGORIES),
        "category_analysis": category_analysis,
    }
