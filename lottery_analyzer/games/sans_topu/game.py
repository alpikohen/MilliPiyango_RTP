from pathlib import Path

from lottery_analyzer.games.sans_topu.analysis import calculate_rtp
from lottery_analyzer.games.sans_topu.rules import (
    RESULTS_URL,
    SELECTED_NUMBERS,
    TICKET_PRICE,
    TOTAL_NUMBERS,
    WAIT_SELECTOR,
)
from lottery_analyzer.models import GameDefinition
from lottery_analyzer.reports.html import generate_html
from lottery_analyzer.sources.winning_list_parser import parse_winning_lists


PROJECT_ROOT = Path(__file__).resolve().parents[3]

SANS_TOPU = GameDefinition(
    slug="sans-topu",
    name="Şans Topu",
    url=RESULTS_URL,
    output_path=PROJECT_ROOT / "sans_topu.html",
    wait_selector=WAIT_SELECTOR,
    total_numbers=TOTAL_NUMBERS,
    selected_numbers=SELECTED_NUMBERS,
    ticket_price=TICKET_PRICE,
    parser=parse_winning_lists,
    analyzer=calculate_rtp,
    reporter=generate_html,
)
