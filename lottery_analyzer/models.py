from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


GameData = List[Dict[str, Any]]
Parser = Callable[[str], GameData]
Analyzer = Callable[[GameData], Optional[Dict[str, Any]]]
Reporter = Callable[..., str]


@dataclass(frozen=True)
class GameDefinition:
    slug: str
    name: str
    url: str
    output_path: Path
    wait_selector: str
    total_numbers: int
    selected_numbers: int
    ticket_price: float
    parser: Parser
    analyzer: Analyzer
    reporter: Reporter
