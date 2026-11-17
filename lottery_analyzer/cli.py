import argparse
from pathlib import Path

from lottery_analyzer.pipeline import run_game
from lottery_analyzer.registry import GAMES, get_game
from lottery_analyzer.reports.summary import generate_summary_html


def main(argv=None):
    parser = argparse.ArgumentParser(description="Milli Piyango çekiliş analizleri")
    game_options = parser.add_mutually_exclusive_group()
    game_options.add_argument("--game", choices=sorted(GAMES), default="super-loto")
    game_options.add_argument("--all", action="store_true", help="Kayıtlı tüm oyunları çalıştır")
    args = parser.parse_args(argv)

    games = list(GAMES.values()) if args.all else [get_game(args.game)]
    results = [run_game(game) for game in games]
    # Başarılı oyunların özetini üret; başarısız olan varsa yine de CLI hata kodu döndür.
    successful_results = [result for result in results if result is not None]
    failed = len(successful_results) != len(results)

    if args.all and successful_results:
        summary_path = Path(__file__).resolve().parents[1] / "index.html"
        summary_html = generate_summary_html(successful_results, summary_path)
        summary_path.write_text(summary_html, encoding="utf-8")
        print(f"✅ Genel RTP raporu kaydedildi: {summary_path}\n")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
