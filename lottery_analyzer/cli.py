import argparse

from lottery_analyzer.pipeline import run_game
from lottery_analyzer.registry import GAMES, get_game


def main(argv=None):
    parser = argparse.ArgumentParser(description="Milli Piyango çekiliş analizleri")
    game_options = parser.add_mutually_exclusive_group()
    game_options.add_argument("--game", choices=sorted(GAMES), default="super-loto")
    game_options.add_argument("--all", action="store_true", help="Kayıtlı tüm oyunları çalıştır")
    args = parser.parse_args(argv)

    games = list(GAMES.values()) if args.all else [get_game(args.game)]
    results = [run_game(game) for game in games]
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
