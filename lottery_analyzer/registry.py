from lottery_analyzer.games.sayisal_loto.game import SAYISAL_LOTO
from lottery_analyzer.games.sayisal_loto_superstar.game import SAYISAL_LOTO_SUPERSTAR
from lottery_analyzer.games.on_numara.game import ON_NUMARA
from lottery_analyzer.games.sans_topu.game import SANS_TOPU
from lottery_analyzer.games.super_loto.game import SUPER_LOTO


GAMES = {
    SUPER_LOTO.slug: SUPER_LOTO,
    SAYISAL_LOTO.slug: SAYISAL_LOTO,
    SAYISAL_LOTO_SUPERSTAR.slug: SAYISAL_LOTO_SUPERSTAR,
    ON_NUMARA.slug: ON_NUMARA,
    SANS_TOPU.slug: SANS_TOPU,
}


def get_game(slug):
    try:
        return GAMES[slug]
    except KeyError as error:
        available = ", ".join(sorted(GAMES))
        raise ValueError(f"Bilinmeyen oyun '{slug}'. Kullanılabilir oyunlar: {available}") from error
