import math
from decimal import Decimal

from lottery_analyzer.games.sayisal_loto.analysis import calculate_probability as calculate_base_probability
from lottery_analyzer.games.sayisal_loto.analysis import calculate_rtp as calculate_base_rtp
from lottery_analyzer.games.sayisal_loto.rules import ALL_CATEGORIES as BASE_CATEGORIES
from lottery_analyzer.games.sayisal_loto_superstar.rules import (
    CATEGORY_ORDER,
    SUPERSTAR_CATEGORIES,
    SUPERSTAR_NUMBERS,
    TICKET_PRICE,
    TOTAL_NUMBERS,
    SELECTED_NUMBERS,
)
from lottery_analyzer.shared.formatting import parse_prize
from lottery_analyzer.shared.tax_calculator import calculate_tax


FIXED_SUPERSTAR_BONUSES = {
    "6": Decimal("40000000"),
    "5+1": Decimal("20000000"),
    "2": Decimal("2500"),
    "1": Decimal("250"),
    "0": Decimal("125"),
}
SUPERSTAR_MULTIPLIERS = {"5": 10, "4": 50, "3": 100}


def calculate_combinations(n, r):
    return math.comb(n, r) if 0 <= r <= n else 0


def calculate_probability(category):
    category = str(category).strip()
    has_superstar = category.endswith("+SüperStar")
    base_category = category[:-len("+SüperStar")] if has_superstar else category
    if base_category not in BASE_CATEGORIES:
        return {"probability": 0, "odds": "İmkansız"}

    # SüperStar bağımsız 90 sayılık çekiliştir; tutma ve tutmama olasılıkları ayrılır.
    base_probability = calculate_base_probability(base_category)["probability"]
    superstar_probability = (
        1 / SUPERSTAR_NUMBERS
        if has_superstar
        else (SUPERSTAR_NUMBERS - 1) / SUPERSTAR_NUMBERS
    )
    probability = base_probability * superstar_probability
    odds = 1 / probability
    odds_text = (
        f"1/{int(odds)}"
        if odds == int(odds)
        else f"1/{odds:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    )
    return {"probability": probability, "odds": odds_text}


def _superstar_bonus(base_category, base_prizes):
    # Çarpanlı kategorilerde bu fonksiyon yalnızca eklenecek farkı döndürür;
    # toplam ödül oluşturulurken normal kategori tutarı ayrıca eklenir.
    if base_category in FIXED_SUPERSTAR_BONUSES:
        return FIXED_SUPERSTAR_BONUSES[base_category]
    multiplier = SUPERSTAR_MULTIPLIERS.get(base_category)
    if multiplier is not None:
        return base_prizes[base_category] * (multiplier - 1)
    return Decimal("0")


def calculate_rtp(data):
    if not data:
        return None

    base_data = []
    superstar_items = []
    # Kaynak sayfa normal ve SüperStar sonuçlarını ayrı bloklarda verir.
    for section in data:
        base_items = [
            item for item in section["items"]
            if item["tutus_sayisi"] in BASE_CATEGORIES
        ]
        if base_items:
            base_data.append({"list_index": section["list_index"], "items": base_items})
        superstar_items.extend(
            item for item in section["items"]
            if item["tutus_sayisi"] in SUPERSTAR_CATEGORIES
        )

    # Normal kategori ödülleri ve 5+1 tahmini, temel oyunun tek doğruluk kaynağından alınır.
    base_analysis = calculate_base_rtp(base_data)
    if base_analysis is None:
        return None

    base_categories = base_analysis["category_analysis"]
    base_prizes = {
        category: Decimal(str(base_categories[category]["prize_per_winner"]))
        for category in BASE_CATEGORIES
    }
    estimated_five_plus_one = base_categories["5+1"].get("label", "5+1").endswith("*")

    category_analysis = {}
    total_return = 0.0
    for base_category in BASE_CATEGORIES:
        base_result = base_categories[base_category]
        base_prize = base_prizes[base_category]
        bonus_prize = _superstar_bonus(base_category, base_prizes)
        base_label = base_result.get("label", base_category)
        superstar_label = f"{base_category}+SüperStar"
        if estimated_five_plus_one and base_category == "5+1":
            superstar_label += "*"

        # Her taban kategori, SüperStar tutulan/tutulmayan iki ayrık sonuca bölünür.
        outcomes = (
            (superstar_label, base_prize + bonus_prize, True),
            (base_label, base_prize, False),
        )
        for label, prize, has_superstar in outcomes:
            category_key = f"{base_category}+SüperStar" if has_superstar else base_category
            probability = calculate_probability(category_key)["probability"]
            expected_value = (float(prize) - calculate_tax(float(prize))) * probability
            category_analysis[category_key] = {
                "label": label,
                "prize_per_winner": float(prize),
                "probability": probability,
                "rtp_percentage": (expected_value / TICKET_PRICE) * 100,
                "return_per_ticket": expected_value,
            }
            total_return += expected_value

    # Ücretli kolon uzayı, ana kombinasyonların her SüperStar seçeneğiyle çarpımıdır.
    total_combinations = calculate_combinations(TOTAL_NUMBERS, SELECTED_NUMBERS) * SUPERSTAR_NUMBERS
    rollover = Decimal(str(base_analysis["devir_amount"]))
    total_prizes = Decimal(str(total_return * total_combinations)) + rollover
    rtp_ratio = float(total_prizes / (total_combinations * TICKET_PRICE))
    superstar_distributed = Decimal("0")
    # Sayfadaki SüperStar ikramiyeleri ek ödüldür; normal dağıtım tutarına ayrıca eklenir.
    for item in superstar_items:
        winners_text = item["kazanan_sayisi"].strip()
        winner_count = int(winners_text) if winners_text.isdigit() else 0
        superstar_distributed += parse_prize(item["odul_text"]) * winner_count

    paid_categories = [
        category for category in category_analysis.values()
        if category["prize_per_winner"] > 0
    ]
    category_rtp_total = sum(category["rtp_percentage"] for category in paid_categories)
    assumption_notes = list(base_analysis.get("assumption_notes", []))
    assumption_notes.append(
        "5, 4 ve 3 + SüperStar kategorilerinin toplam ikramiyesi sırasıyla normal "
        "kategori ikramiyesinin 10, 50 ve 100 katıdır; diğer tanımlı SüperStar "
        "ek ikramiyeleri normal kategori ödülüne eklenmiştir."
    )

    return {
        "total_combinations": total_combinations,
        "combination_formula": "C(90, 6) × 90",
        "total_prizes": float(total_prizes),
        "scraped_total_prizes": float(
            Decimal(str(base_analysis["scraped_total_prizes"])) + superstar_distributed
        ),
        "devir_amount": float(rollover),
        "rtp_percentage": rtp_ratio * 100,
        "category_rtp_total": category_rtp_total,
        "return_per_ticket": float(total_return),
        "ticket_price": TICKET_PRICE,
        "category_order": list(CATEGORY_ORDER),
        "category_analysis": category_analysis,
        "assumption_notes": assumption_notes,
    }
