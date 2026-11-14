import re
from datetime import datetime

from bs4 import BeautifulSoup


TURKISH_MONTHS = {
    "ocak": 1,
    "şubat": 2,
    "mart": 3,
    "nisan": 4,
    "mayıs": 5,
    "haziran": 6,
    "temmuz": 7,
    "ağustos": 8,
    "eylül": 9,
    "ekim": 10,
    "kasım": 11,
    "aralık": 12,
}
TURKISH_WEEKDAYS = (
    "Pazartesi",
    "Salı",
    "Çarşamba",
    "Perşembe",
    "Cuma",
    "Cumartesi",
    "Pazar",
)


def extract_draw_datetime(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    date_pattern = re.compile(
        r"(\d{1,2})\s+([\wÇĞİÖŞÜçğıöşü]+)\s+(\d{4})\s+(\d{1,2}:\d{2})",
        re.IGNORECASE,
    )

    for heading in soup.find_all("h1"):
        match = date_pattern.search(heading.get_text(" ", strip=True))
        if not match:
            continue

        day, month_name, year, time_text = match.groups()
        month = TURKISH_MONTHS.get(month_name.casefold())
        if month is None:
            continue

        draw_datetime = datetime.strptime(
            f"{day} {month} {year} {time_text}",
            "%d %m %Y %H:%M",
        )
        weekday = TURKISH_WEEKDAYS[draw_datetime.weekday()]
        return f"{weekday}, {int(day)} {month_name} {year} {time_text}"

    return ""


def parse_winning_lists(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    winning_lists = soup.find_all(class_="winning-list")
    all_data = []

    for index, winning_list in enumerate(winning_lists):
        rows = winning_list.find_all("div", class_=lambda value: value and "row" in value.split())
        list_data = {"list_index": index + 1, "items": []}
        for row in rows:
            columns = row.find_all("div", class_=lambda value: value and "col-" in value)
            if len(columns) >= 3:
                list_data["items"].append({
                    "tutus_sayisi": columns[0].get_text(strip=True),
                    "kazanan_sayisi": columns[1].get("data-value", ""),
                    "kazanan_text": columns[1].get_text(strip=True),
                    "odul_fiyati": columns[2].get("data-price", ""),
                    "odul_text": columns[2].get_text(strip=True),
                })
        if list_data["items"]:
            all_data.append(list_data)

    return all_data