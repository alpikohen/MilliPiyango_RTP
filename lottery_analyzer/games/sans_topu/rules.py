TOTAL_NUMBERS = 34
SELECTED_NUMBERS = 5
DRAWN_NUMBERS = 5
BONUS_NUMBERS = 14
TICKET_PRICE = 15
WINNING_CATEGORIES = (
    "5+1",
    "5",
    "4+1",
    "4",
    "3+1",
    "3",
    "2+1",
    "1+1",
    "0+1",
)
ALL_CATEGORIES = tuple(
    category
    for matches in range(SELECTED_NUMBERS, -1, -1)
    for category in (f"{matches}+1", str(matches))
)
RESULTS_URL = "https://www.millipiyangoonline.com/sans-topu/cekilis-sonuclari.91.2026"
WAIT_SELECTOR = "winning-list"
