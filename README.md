# Milli Piyango Oyun Analizleri

Milli Piyango oyunlarının çekiliş sonuçlarını Selenium ile alan, oyun kurallarına özel analiz yapan ve HTML raporları üreten bir Python projesi. Şu anda Süper Loto kayıtlıdır; yeni oyunlar `lottery_analyzer/games/` altına eklenebilir.

## Neden?

Çekiliş verilerini ortak kaynak katmanıyla almak, her oyunun kendi matematiksel kurallarını ayrı tutmak ve sonuçları aynı raporlama akışıyla sunmak.

## Özellikler

- Selenium ile Milli Piyango sayfalarından veri alma
- Oyun başına parser ve analiz kuralları
- Ortak pipeline, oyun kayıt sistemi ve HTML raporu
- Bir oyunu veya kayıtlı tüm oyunları çalıştırma

## Gereksinimler

- Python 3.8+
- Google Chrome
- Selenium 4 (Selenium Manager uygun ChromeDriver'ı yönetir)

## Kurulum

```powershell
pip install selenium beautifulsoup4
```

## Çalıştırma

```powershell
cd C:\Users\ASUS\Desktop\MilliPiyango_RTP
python run.py --game super-loto
```

Tüm kayıtlı oyunları çalıştırmak için:

```powershell
python run.py --all
```

Çıktı: `cekilis_sonuclari.html` proje kökünde oluşturulur.

## Proje Yapısı

```
MilliPiyango_RTP/
├── run.py
├── lottery_analyzer/
│   ├── cli.py
│   ├── models.py
│   ├── pipeline.py
│   ├── registry.py
│   ├── sources/
│   │   └── selenium_source.py
│   ├── games/
│   │   └── super_loto/
│   │       ├── game.py
│   │       ├── parser.py
│   │       ├── rules.py
│   │       └── analysis.py
│   ├── reports/
│   │   └── html.py
│   └── shared/
│       ├── formatting.py
│       └── tax_calculator.py
└── cekilis_sonuclari.html
```