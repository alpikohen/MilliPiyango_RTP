import re

from lottery_analyzer.games.sayisal_loto.parser import parse_results as parse_base_results
from lottery_analyzer.games.sayisal_loto_superstar.rules import SUPERSTAR_CATEGORIES
from lottery_analyzer.sources.winning_list_parser import parse_winning_lists


JOKER_ANNOTATION = re.compile(r"\s*\(joker\)\s*\*?", re.IGNORECASE)


def parse_superstar_results(page_source):
    # Temel parser normal bloğu ayıklar; aşağıda yalnızca SüperStar bloğu eklenir.
    results = parse_base_results(page_source)
    superstar_sections = []

    for section in parse_winning_lists(page_source):
        items = []
        for source_item in section["items"]:
            label = str(source_item["tutus_sayisi"]).strip()
            if "süperstar" not in label.casefold():
                continue

            # Joker açıklamasını temizleyip raporda kullanılan kanonik kategori anahtarını oluştur.
            category = JOKER_ANNOTATION.sub("", label)
            category = re.sub(r"\s+", "", category).replace("*", "")
            if category not in SUPERSTAR_CATEGORIES:
                continue

            item = dict(source_item)
            item["tutus_sayisi"] = category
            items.append(item)

        if items:
            superstar_sections.append({"list_index": section["list_index"], "items": items})

    return results + superstar_sections
