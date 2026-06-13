from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

from rtp_calculation import calculate_rtp
from html_reporter import generate_html


OUTPUT_FILE = "cekilis_sonuclari.html"
URL = "https://www.millipiyangoonline.com/super-loto/cekilis-sonuclari.65.2026"


def scrape_winning_list():
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(service=Service(), options=options)
        driver.get(URL)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "winning-list"))
        )
        driver.implicitly_wait(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        winning_lists = soup.find_all(class_="winning-list")
        if not winning_lists:
            print("❌ 'winning-list' class'ı bulunamadı!")
            return []
        all_data = []
        for idx, winning_list in enumerate(winning_lists):
            rows = winning_list.find_all("div", class_=lambda x: x and "row" in x.split())
            list_data = {"list_index": idx + 1, "items": []}
            for row in rows:
                cols = row.find_all("div", class_=lambda x: x and "col-" in x)
                if len(cols) >= 3:
                    list_data["items"].append({
                        "tunus_sayisi": cols[0].get_text(strip=True),
                        "kazanan_sayisi": cols[1].get("data-value", ""),
                        "kazanan_text": cols[1].get_text(strip=True),
                        "odul_fiyati": cols[2].get("data-price", ""),
                        "odul_text": cols[2].get_text(strip=True),
                    })
            if list_data["items"]:
                all_data.append(list_data)
        return all_data
    except Exception as e:
        print(f"❌ Hata: {e}")
        return []
    finally:
        if driver:
            driver.quit()


def main():
    print("🎯 Milli Piyango Web Scraper Başlatılıyor...\n")
    data = scrape_winning_list()
    if not data:
        print("\n❌ Veri alınamadı!")
        return
    print(f"\n✅ {len(data)} liste bulundu!")
    rtp_data = calculate_rtp(data)
    html_content = generate_html(data, rtp_data)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ HTML kaydedildi: {OUTPUT_FILE}\n")


if __name__ == "__main__":
    main()
