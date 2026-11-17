from lottery_analyzer.games.sayisal_loto.rules import (
    ALL_CATEGORIES as BASE_CATEGORIES,
    RESULTS_URL,
    SELECTED_NUMBERS,
    TOTAL_NUMBERS,
    WAIT_SELECTOR,
)

BASE_TICKET_PRICE = 25
SUPERSTAR_TICKET_PRICE = 15
TICKET_PRICE = BASE_TICKET_PRICE + SUPERSTAR_TICKET_PRICE
SUPERSTAR_NUMBERS = 90
SUPERSTAR_CATEGORIES = tuple(f"{category}+SüperStar" for category in BASE_CATEGORIES)
CATEGORY_ORDER = tuple(
    label
    for category in BASE_CATEGORIES
    for label in (f"{category}+SüperStar", category)
)
