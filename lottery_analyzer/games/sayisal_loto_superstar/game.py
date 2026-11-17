from pathlib import Path

from lottery_analyzer.games.sayisal_loto_superstar.analysis import calculate_rtp
from lottery_analyzer.games.sayisal_loto_superstar.parser import parse_superstar_results
from lottery_analyzer.games.sayisal_loto_superstar.rules import (
    RESULTS_URL,
    SELECTED_NUMBERS,
    TICKET_PRICE,
    TOTAL_NUMBERS,
    WAIT_SELECTOR,
)
from lottery_analyzer.models import GameDefinition
from lottery_analyzer.reports.html import generate_html


PROJECT_ROOT = Path(__file__).resolve().parents[3]

SAYISAL_LOTO_SUPERSTAR = GameDefinition(
    slug="sayisal-loto-superstar",
    name="Çılgın Sayısal Loto + SüperStar",
    url=RESULTS_URL,
    output_path=PROJECT_ROOT / "sayisal_loto_superstar.html",
    wait_selector=WAIT_SELECTOR,
    total_numbers=TOTAL_NUMBERS,
    selected_numbers=SELECTED_NUMBERS,
    ticket_price=TICKET_PRICE,
    parser=parse_superstar_results,
    analyzer=calculate_rtp,
    reporter=generate_html,
)
