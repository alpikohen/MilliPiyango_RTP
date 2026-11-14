from lottery_analyzer.games.on_numara.game import ON_NUMARA
from lottery_analyzer.games.super_loto.game import SUPER_LOTO


GAMES = {
    SUPER_LOTO.slug: SUPER_LOTO,
    ON_NUMARA.slug: ON_NUMARA,
}


def get_game(slug):
    try:
        return GAMES[slug]
    except KeyError as error:
        available = ", ".join(sorted(GAMES))
        raise ValueError(f"Bilinmeyen oyun '{slug}'. Kullanılabilir oyunlar: {available}") from error
