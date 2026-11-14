from datetime import datetime

from lottery_analyzer.shared.formatting import tr_num
from lottery_analyzer.shared.tax_calculator import calculate_tax


def generate_html(
    data,
    rtp_data=None,
    draw_info="",
    game_name="Süper Loto",
    draw_datetime="",
    total_numbers=60,
    selected_numbers=6,
    ticket_price=25,
):
    html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Milli Piyango Çekiliş Sonuçları</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; border-radius: 10px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header p {{ font-size: 14px; opacity: 0.9; }}
        .content {{ padding: 30px; }}
        .winning-section {{ margin-bottom: 30px; border: 2px solid #e0e0e0; border-radius: 8px; padding: 20px; background: #f9f9f9; }}
        .section-title {{ font-size: 18px; font-weight: bold; color: #333; margin-bottom: 15px; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
        .no-data {{ text-align: center; padding: 40px; color: #999; font-size: 16px; }}
        .footer {{ background: #f0f0f0; padding: 20px; text-align: center; color: #666; font-size: 12px; }}
        .rtp-section {{ margin-bottom: 30px; border: 3px solid #28a745; border-radius: 8px; padding: 20px; background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%); }}
        .rtp-title {{ font-size: 20px; font-weight: bold; color: #1b5e20; margin-bottom: 20px; text-align: center; }}
        .rtp-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .rtp-item {{ background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745; text-align: center; }}
        .rtp-label {{ font-size: 12px; color: #666; font-weight: bold; margin-bottom: 5px; }}
        .rtp-value {{ font-size: 20px; font-weight: bold; color: #28a745; }}
        .rtp-subtext {{ font-size: 11px; color: #999; margin-top: 5px; }}
        .category-analysis {{ margin-top: 30px; padding: 20px; background: linear-gradient(135deg, #f5f9ff 0%, #f0f8ff 100%); border: 2px solid #4a90e2; border-radius: 8px; }}
        .category-title {{ font-size: 16px; font-weight: bold; color: #1a4d8a; margin-bottom: 15px; }}
        .category-table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; }}
        .category-table thead {{ background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%); color: white; }}
        .category-table th {{ padding: 12px; text-align: center; font-weight: bold; font-size: 12px; }}
        .category-table td {{ padding: 12px; text-align: center; border-bottom: 1px solid #e0e0e0; font-size: 12px; }}
        .category-table tbody tr:hover {{ background: #f9f9f9; }}
        .category-table .tunus {{ font-weight: bold; color: #1a4d8a; }}
        .category-table .highlight-contribution {{ background: #fff3cd; font-weight: bold; color: #856404; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎰 Milli Piyango Çekiliş Sonuçları</h1>
            <p>{game_name} - {draw_info} - Çekiliş zamanı: {draw_datetime or 'Alınamadı'}</p>
        </div>
        <div class="content">
"""

    if rtp_data:
        rtp_percentage = rtp_data["rtp_percentage"]
        category_total = tr_num(rtp_data.get("category_rtp_total", rtp_percentage), 2)
        return_per_ticket = rtp_data.get("return_per_ticket", rtp_data.get("return_per_25tl", 0))
        return_per_ticket_text = tr_num(return_per_ticket, 2)
        total_prize = tr_num(rtp_data.get("scraped_total_prizes", rtp_data["total_prizes"]), 2)
        rollover_prize = tr_num(rtp_data["devir_amount"], 2)
        total_combinations = f"{rtp_data['total_combinations']:,}".replace(",", ".")

        html_content += f"""            <div class="rtp-section">
                <div class="rtp-title">📊 Return to Player (RTP) Analizi</div>
                <div class="rtp-grid">
                    <div class="rtp-item"><div class="rtp-label">RTP Oranı</div><div class="rtp-value">{category_total}%</div><div class="rtp-subtext">Oyuncuya geri dönüş</div></div>
                    <div class="rtp-item"><div class="rtp-label">Toplam İkramiye</div><div class="rtp-value">{total_prize} ₺</div><div class="rtp-subtext">Devir dahil</div></div>
                    <div class="rtp-item"><div class="rtp-label">Devir Tutarı</div><div class="rtp-value">{rollover_prize} ₺</div><div class="rtp-subtext">Sonraki çekilişe</div></div>
                    <div class="rtp-item"><div class="rtp-label">Olası Kombinasyon</div><div class="rtp-value">{total_combinations}</div><div class="rtp-subtext">C({total_numbers}, {selected_numbers})</div></div>
                    <div class="rtp-item"><div class="rtp-label">Bilet Fiyatı</div><div class="rtp-value">{tr_num(ticket_price, 2)} ₺</div></div>
                    <div class="rtp-item"><div class="rtp-label">{tr_num(ticket_price, 2)} TL Karşılığı</div><div class="rtp-value">{return_per_ticket_text} ₺</div></div>
                </div>
                <div style="margin-top: 20px; padding: 15px; background: white; border-radius: 8px; font-size: 13px; color: #333; border-left: 4px solid #28a745;">
                    <strong>💡 Açıklama:</strong> Her {tr_num(ticket_price, 2)} TL'lik bilet oynadığında, ortalama olarak <strong>{return_per_ticket_text} TL</strong> geri kazanırsınız.
                </div>
            </div>
"""

    if rtp_data and rtp_data.get("category_analysis"):
        html_content += f"""            <div class="category-analysis">
                <div class="category-title">📈 Detaylı RTP Analizi</div>
                <table class="category-table">
                    <thead><tr><th>Kategori</th><th>Birim Ödül (₺)</th><th>Veraset ve İntikal Vergisi (₺)</th><th>Net Ödül (TL)</th><th>Olasılık</th><th>RTP Yüzdesi (%)</th><th>{tr_num(ticket_price, 2)} TL Başına Getiri (₺)</th></tr></thead>
                    <tbody>
"""
        for matched in sorted(rtp_data["category_analysis"].keys(), reverse=True):
            category = rtp_data["category_analysis"][matched]
            prize_text = tr_num(category["prize_per_winner"], 2)
            tax_amount = calculate_tax(category["prize_per_winner"])
            tax_text = tr_num(tax_amount, 2)
            net_prize_text = tr_num(category["prize_per_winner"] - tax_amount, 2)
            probability = category.get("probability", 0)

            if probability > 0:
                odds = 1 / probability
                denominator = (
                    f"{int(odds):,}".replace(",", ".")
                    if odds == int(odds)
                    else f"{odds:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
                )
                probability_text = f"1/{denominator}"
            else:
                probability_text = "N/A"

            rtp_text = tr_num(category["rtp_percentage"], 4) + "%"
            category_return = category.get("return_per_ticket", category.get("return_per_25tl", 0))
            return_text = tr_num(category_return, 4)
            html_content += f"""                        <tr>
                            <td class="tunus">{matched}</td><td>{prize_text}</td><td>{tax_text}</td><td>{net_prize_text}</td>
                            <td>{probability_text}</td><td class="highlight-contribution">{rtp_text}</td><td>{return_text}</td>
                        </tr>
"""

        non_zero_categories = [
            category for category in rtp_data["category_analysis"].values()
            if category["prize_per_winner"] > 0
        ]
        total_return = sum(
            category.get("return_per_ticket", category.get("return_per_25tl", 0))
            for category in non_zero_categories
        )
        total_rtp_text = tr_num(rtp_data.get("category_rtp_total", rtp_percentage), 4) + "%"
        total_return_text = tr_num(total_return, 4)
        html_content += f"""                        <tr class="highlight-contribution">
                            <td><strong>TOPLAM</strong></td><td><strong>-</strong></td><td><strong>-</strong></td>
                            <td><strong>-</strong></td><td><strong>1/1</strong></td><td><strong>{total_rtp_text}</strong></td>
                            <td><strong>{total_return_text}</strong></td>
                        </tr>
                    </tbody>
                </table>
            </div>
"""

    if data:
        html_content += """            <div class="winning-section">
                <div class="section-title">Kazanan Kategoriler</div>
                <table class="category-table">
                    <thead>
                        <tr>
                            <th>Tutturulan Sayı</th>
                            <th>Kazanan Kişi Sayısı</th>
                            <th>Kişi Başı İkramiye</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for section in data:
            for item in section["items"]:
                winner_text = item.get("kazanan_text") or item.get("kazanan_sayisi", "")
                html_content += f"""                        <tr>
                            <td class="tunus">{item['tutus_sayisi']}</td>
                            <td>{winner_text}</td>
                            <td>{item['odul_text']}</td>
                        </tr>
"""
        html_content += """                    </tbody>
                </table>
            </div>
"""
    else:
        html_content += """            <div class="no-data"><p>⚠️ Veri alınamadı. Lütfen daha sonra tekrar deneyiniz.</p></div>
"""

    html_content += """        </div>
        <div class="footer">
            <p>Bu sayfa otomatik olarak oluşturulmuştur. Son güncelleme: """ + datetime.now().strftime("%d.%m.%Y %H:%M:%S") + """</p>
        </div>
    </div>
</body>
</html>
"""
    return html_content
