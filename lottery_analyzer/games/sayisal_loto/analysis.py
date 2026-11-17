import math
from decimal import Decimal

from lottery_analyzer.games.sayisal_loto.rules import (
    ALL_CATEGORIES,
    DRAWN_NUMBERS,
    JOKER_NUMBERS,
    SELECTED_NUMBERS,
    TICKET_PRICE,
    TOTAL_NUMBERS,
)
from lottery_analyzer.shared.formatting import parse_prize, tr_num
from lottery_analyzer.shared.tax_calculator import calculate_tax


def calculate_combinations(n, r):
    return math.comb(n, r) if 0 <= r <= n else 0


def calculate_probability(category):
    category = str(category).strip()
    total_combinations = calculate_combinations(TOTAL_NUMBERS, SELECTED_NUMBERS)
    other_drawn_numbers = TOTAL_NUMBERS - DRAWN_NUMBERS - JOKER_NUMBERS

    if category == "5+1":
        favorable_combinations = (
            calculate_combinations(DRAWN_NUMBERS, 5)
            * calculate_combinations(JOKER_NUMBERS, 1)
        )
    elif category == "5":
        favorable_combinations = (
            calculate_combinations(DRAWN_NUMBERS, 5)
            * calculate_combinations(other_drawn_numbers, 1)
        )
    elif category in ALL_CATEGORIES:
        matched = int(category)
        favorable_combinations = (
            calculate_combinations(DRAWN_NUMBERS, matched)
            * calculate_combinations(TOTAL_NUMBERS - DRAWN_NUMBERS, SELECTED_NUMBERS - matched)
        )
    else:
        return {"probability": 0, "odds": "İmkansız"}

    probability = favorable_combinations / total_combinations
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

    total_combinations = calculate_combinations(TOTAL_NUMBERS, SELECTED_NUMBERS)
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
    all_items = [item for section in data for item in section["items"]]
    five_plus_one_item = next(
        (item for item in all_items if item["tutus_sayisi"] == "5+1"),
        None,
    )
    five_item = next(
        (item for item in all_items if item["tutus_sayisi"] == "5"),
        None,
    )
    estimated_five_plus_one = None
    assumptions = []

    if (
        five_plus_one_item is not None
        and five_plus_one_item["kazanan_sayisi"].strip().isdigit()
        and int(five_plus_one_item["kazanan_sayisi"].strip()) == 0
        and five_item is not None
    ):
        five_winner_count_text = five_item["kazanan_sayisi"].strip()
        five_winner_count = int(five_winner_count_text) if five_winner_count_text.isdigit() else 0
        five_prize_per_winner = parse_prize(five_item["odul_text"])
        five_distributed_total = five_prize_per_winner * five_winner_count
        estimated_five_plus_one = (
            five_distributed_total * Decimal(13) / Decimal(8)
            + Decimal(10_000_000)
        )
        assumptions.append(
            "* 5+1 ikramiyesi, 5 kategorisinde dağıtılan toplam tutar "
            f"({tr_num(five_distributed_total, 2)} TL) × 13/8 + 10.000.000 TL "
            f"formülüyle {tr_num(estimated_five_plus_one, 2)} TL varsayılmıştır; "
            "5+1 kategorisinde kazanan olmadığı için bu tutar tahminidir."
        )

    for item in all_items:
        category_name = str(item["tutus_sayisi"]).strip()
        if category_name not in category_analysis:
            continue

        prize = parse_prize(item["odul_text"])
        winners_text = item["kazanan_sayisi"].strip()
        winner_count = int(winners_text) if winners_text.isdigit() else 0
        scraped_total_prizes += float(prize) * winner_count

        category_label = category_name
        if category_name == "5+1" and winner_count == 0 and estimated_five_plus_one is not None:
            prize = estimated_five_plus_one
            category_label = "5+1*"

        probability = calculate_probability(category_name)["probability"]
        expected_value = (float(prize) - calculate_tax(float(prize))) * probability
        rtp_percentage = (expected_value / TICKET_PRICE) * 100

        if item.get("kazanan_text", "").strip().casefold() == "devir":
            rollover = max(rollover, prize)

        category_analysis[category_name] = {
            "label": category_label,
            "prize_per_winner": float(prize),
            "probability": probability,
            "rtp_percentage": rtp_percentage,
            "return_per_ticket": expected_value,
        }
        total_return += expected_value

    total_prizes = Decimal(str(total_return * total_combinations)) + rollover
    rtp_ratio = float(total_prizes / (total_combinations * TICKET_PRICE))
    paid_categories = [
        category for category in category_analysis.values()
        if category["prize_per_winner"] > 0
    ]
    category_rtp_total = sum(category["rtp_percentage"] for category in paid_categories)

    return {
        "total_combinations": total_combinations,
        "combination_formula": "C(90, 6)",
        "total_prizes": float(total_prizes),
        "scraped_total_prizes": scraped_total_prizes + float(rollover),
        "devir_amount": float(rollover),
        "rtp_percentage": rtp_ratio * 100,
        "category_rtp_total": category_rtp_total,
        "return_per_ticket": float(total_return),
        "ticket_price": TICKET_PRICE,
        "category_order": list(ALL_CATEGORIES),
        "category_analysis": category_analysis,
        "assumption_notes": assumptions,
    }
