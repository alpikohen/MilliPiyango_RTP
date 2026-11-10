import re

from lottery_analyzer.sources.selenium_source import fetch_page_source


def _draw_info(url):
    match = re.search(r"\.(\d+)\.(\d+)", url)
    if match:
        return f"Çekiliş #{match.group(1)} / {match.group(2)}"
    return "Bilinmeyen Çekiliş"


def run_game(game):
    print(f"🎯 {game.name} analizi başlatılıyor...\n")
    try:
        page_source = fetch_page_source(game.url, game.wait_selector)
        data = game.parser(page_source)
    except Exception as error:
        print(f"❌ Hata: {error}")
        return False

    if not data:
        print("\n❌ Veri alınamadı!")
        return False

    print(f"\n✅ {len(data)} liste bulundu!")
    analysis = game.analyzer(data)
    html_content = game.reporter(
        data,
        analysis,
        _draw_info(game.url),
        game_name=game.name,
        total_numbers=game.total_numbers,
        selected_numbers=game.selected_numbers,
        ticket_price=game.ticket_price,
    )
    game.output_path.parent.mkdir(parents=True, exist_ok=True)
    game.output_path.write_text(html_content, encoding="utf-8")
    print(f"✅ HTML kaydedildi: {game.output_path}\n")
    return True
