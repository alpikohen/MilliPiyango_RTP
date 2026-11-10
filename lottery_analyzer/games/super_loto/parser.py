from bs4 import BeautifulSoup


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
                    "tunus_sayisi": columns[0].get_text(strip=True),
                    "kazanan_sayisi": columns[1].get("data-value", ""),
                    "kazanan_text": columns[1].get_text(strip=True),
                    "odul_fiyati": columns[2].get("data-price", ""),
                    "odul_text": columns[2].get_text(strip=True),
                })
        if list_data["items"]:
            all_data.append(list_data)

    return all_data
