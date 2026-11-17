# Milli Piyango Oyun Analizleri

Milli Piyango oyunlarının çekiliş sonuçlarını Selenium ile alan, oyun kurallarına özel analiz yapan ve HTML raporları üreten bir Python projesi. Süper Loto, On Numara, Şans Topu ve Çılgın Sayısal Loto kayıtlıdır; yeni oyunlar `lottery_analyzer/games/` altına eklenebilir.

## Neden?

Çekiliş verilerini ortak kaynak katmanıyla almak, her oyunun kendi matematiksel kurallarını ayrı tutmak ve sonuçları aynı raporlama akışıyla sunmak.

## Özellikler

- Selenium ile Milli Piyango sayfalarından veri alma
- Ortak Selenium/veri parse katmanı ve oyun başına analiz kuralları
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
python run.py --game on-numara
python run.py --game sans-topu
python run.py --game sayisal-loto
python run.py --game sayisal-loto-superstar
```

Tüm kayıtlı oyunları çalıştırmak ve RTP sıralamalı genel raporu üretmek için:

```powershell
python run.py --all
```

Tekil komutlar `super_loto.html`, `on_numara.html`, `sans_topu.html`, `sayisal_loto.html` ve `sayisal_loto_superstar.html` raporlarını üretir. Sayısal Loto SüperStar seçeneği ayrı bir oyun olarak hesaplanır; kolon bedeli 40 TL'dir. `--all` tüm raporlara bağlantı içeren RTP özetini de üretir.

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
│   │   ├── selenium_source.py
│   │   └── winning_list_parser.py
│   ├── games/
│   │   ├── super_loto/
│   │   │   ├── game.py
│   │   │   ├── rules.py
│   │   │   └── analysis.py
│   │   ├── on_numara/
│   │   │   ├── game.py
│   │   │   ├── rules.py
│   │   │   └── analysis.py
│   │   ├── sans_topu/
│   │   │   ├── game.py
│   │   │   ├── rules.py
│   │   │   └── analysis.py
│   │   ├── sayisal_loto/
│   │   │   ├── game.py
│   │   │   ├── parser.py
│   │   │   ├── rules.py
│   │   │   └── analysis.py
│   │   ├── sayisal_loto_superstar/
│   │   │   ├── game.py
│   │   │   ├── parser.py
│   │   │   ├── rules.py
│   │   │   └── analysis.py
│   ├── reports/
│   │   ├── html.py
│   │   └── summary.py
│   └── shared/
│       ├── formatting.py
│       └── tax_calculator.py
├── super_loto.html
├── on_numara.html
├── sans_topu.html
├── sayisal_loto.html
├── sayisal_loto_superstar.html
└── index.html
```