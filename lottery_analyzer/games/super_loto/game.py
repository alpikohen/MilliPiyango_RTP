from pathlib import Path

from lottery_analyzer.games.super_loto.analysis import calculate_rtp
from lottery_analyzer.games.super_loto.parser import parse_winning_lists
from lottery_analyzer.games.super_loto.rules import (
    RESULTS_URL,
    SELECTED_NUMBERS,
    TICKET_PRICE,
    TOTAL_NUMBERS,
    WAIT_SELECTOR,
)
from lottery_analyzer.models import GameDefinition
from lottery_analyzer.reports.html import generate_html


PROJECT_ROOT = Path(__file__).resolve().parents[3]

SUPER_LOTO = GameDefinition(
    slug="super-loto",
    name="Super Loto 2026",
    url=RESULTS_URL,
    output_path=PROJECT_ROOT / "cekilis_sonuclari.html",
    wait_selector=WAIT_SELECTOR,
    total_numbers=TOTAL_NUMBERS,
    selected_numbers=SELECTED_NUMBERS,
    ticket_price=TICKET_PRICE,
    parser=parse_winning_lists,
    analyzer=calculate_rtp,
    reporter=generate_html,
)
