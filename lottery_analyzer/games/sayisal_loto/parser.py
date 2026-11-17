import re

from lottery_analyzer.games.sayisal_loto.rules import ALL_CATEGORIES
from lottery_analyzer.sources.winning_list_parser import parse_winning_lists


JOKER_LABEL = re.compile(r"\s*\(joker\)\s*\*?\s*$", re.IGNORECASE)


def parse_results(page_source):
    parsed_lists = parse_winning_lists(page_source)
    results = []

    for section in parsed_lists:
        filtered_items = []
        for source_item in section["items"]:
            label = str(source_item["tutus_sayisi"]).strip()
            # Normal oyun raporuna SüperStar'ın ayrı kategori bloğu karışmamalıdır.
            if "süperstar" in label.casefold():
                continue

            # Sayfadaki açıklama/yıldız işaretini normalize edip Joker kategorisini koru.
            category = JOKER_LABEL.sub("", label).replace("*", "").strip()
            if category not in ALL_CATEGORIES:
                continue

            item = dict(source_item)
            item["tutus_sayisi"] = category
            filtered_items.append(item)

        if filtered_items:
            results.append({"list_index": section["list_index"], "items": filtered_items})

    return results
