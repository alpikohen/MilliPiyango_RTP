# Milli Piyango Super Loto - RTP Analizi

Milli Piyango Super Loto çekiliş sonuçlarını otomatik olarak çeken, detaylı Return to Player (RTP) analizi sunan bir Python aracı.

## Neden?

Super Loto'nun gerçek oyuncuya dönüş oranını (RTP) ölçmek için. Olasılık tabanlı beklenti değeri analizi ile her 25 TL'lik biletin teorik getirisini hesaplar.

## Özellikler

- 🎯 Selenium ile canlı çekiliş verisi çekme
- 📊 Detaylı RTP Analizi tablosu (0–6 tutuş kategorisi)
- 🧮 Olasılıklar ve beklenen değerler (expected value)
- 🏆 Devir tutarları dahil toplam ödül hesaplama
- 📄 Otomatik HTML raporu üretme

## Gereksinimler

- Python 3.8+
- Google Chrome
- ChromeDriver (PATH'te olmalı)

## Kurulum

```powershell
pip install selenium beautifulsoup4
```

## Çalıştırma

```powershell
cd C:\Users\ASUS\Desktop\MilliPiyango_RTP
python run.py
```

Çıktı: `cekilis_sonuclari.html` dosyası oluşturulur.

## Proje Yapısı

```
MilliPiyango_RTP/
├── run.py               # Giriş noktası
├── web_scraper.py       # Selenium ile veri çekme
├── rtp_calculation.py   # RTP ve olasılık hesaplamaları
├── html_reporter.py     # HTML raporu üretimi
├── utils.py             # Yardımcı fonksiyonlar
├── __init__.py
└── cekilis_sonuclari.html
```