from pathlib import Path

from lottery_analyzer.games.sayisal_loto.analysis import calculate_rtp
from lottery_analyzer.games.sayisal_loto.parser import parse_results
from lottery_analyzer.games.sayisal_loto.rules import (
    RESULTS_URL,
    SELECTED_NUMBERS,
    TICKET_PRICE,
    TOTAL_NUMBERS,
    WAIT_SELECTOR,
)
from lottery_analyzer.models import GameDefinition
from lottery_analyzer.reports.html import generate_html


PROJECT_ROOT = Path(__file__).resolve().parents[3]

SAYISAL_LOTO = GameDefinition(
    slug="sayisal-loto",
    name="Çılgın Sayısal Loto",
    url=RESULTS_URL,
    output_path=PROJECT_ROOT / "sayisal_loto.html",
    wait_selector=WAIT_SELECTOR,
    total_numbers=TOTAL_NUMBERS,
    selected_numbers=SELECTED_NUMBERS,
    ticket_price=TICKET_PRICE,
    parser=parse_results,
    analyzer=calculate_rtp,
    reporter=generate_html,
)
