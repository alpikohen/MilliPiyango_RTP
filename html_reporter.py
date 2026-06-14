from datetime import datetime
from tax_calculator import calculate_tax

from rtp_calculation import TOTAL_NUMBERS, SELECTED_NUMBERS, TICKET_PRICE, calculate_probability
from utils import tr_num


def generate_html(data, rtp_data=None, draw_info=""):
    html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Milli Piyango Çekiliş Sonuçları</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header p {{ font-size: 14px; opacity: 0.9; }}
        .content {{ padding: 30px; }}
        .winning-section {{
            margin-bottom: 30px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            background: #f9f9f9;
        }}
        .section-title {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        .items-list {{ list-style: none; }}
        .list-item {{
            padding: 12px;
            margin: 8px 0;
            background: white;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }}
        .item-details {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .item-row {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .item-row .label {{
            font-weight: bold;
            color: #666;
            min-width: 70px;
            font-size: 12px;
        }}
        .item-row .value {{
            flex: 1;
            color: #333;
            font-size: 14px;
        }}
        .item-row .value.highlight {{
            background: #667eea;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
        }}
        .item-row .raw-value {{
            color: #999;
            font-size: 11px;
            margin-left: auto;
        }}
        .no-data {{
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 16px;
        }}
        .footer {{
            background: #f0f0f0;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 12px;
        }}
        .rtp-section {{
            margin-bottom: 30px;
            border: 3px solid #28a745;
            border-radius: 8px;
            padding: 20px;
            background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
        }}
        .rtp-title {{
            font-size: 20px;
            font-weight: bold;
            color: #1b5e20;
            margin-bottom: 20px;
            text-align: center;
        }}
        .rtp-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        .rtp-item {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #28a745;
            text-align: center;
        }}
        .rtp-label {{
            font-size: 12px;
            color: #666;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .rtp-value {{
            font-size: 20px;
            font-weight: bold;
            color: #28a745;
        }}
        .rtp-subtext {{
            font-size: 11px;
            color: #999;
            margin-top: 5px;
        }}
        .category-analysis {{
            margin-top: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #f5f9ff 0%, #f0f8ff 100%);
            border: 2px solid #4a90e2;
            border-radius: 8px;
        }}
        .category-title {{
            font-size: 16px;
            font-weight: bold;
            color: #1a4d8a;
            margin-bottom: 15px;
        }}
        .category-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
        }}
        .category-table thead {{
            background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
            color: white;
        }}
        .category-table th {{
            padding: 12px;
            text-align: center;
            font-weight: bold;
            font-size: 12px;
        }}
        .category-table td {{
            padding: 12px;
            text-align: center;
            border-bottom: 1px solid #e0e0e0;
            font-size: 12px;
        }}
        .category-table tbody tr:hover {{ background: #f9f9f9; }}
        .category-table .tunus {{
            font-weight: bold;
            color: #1a4d8a;
        }}
        .category-table .highlight-contribution {{
            background: #fff3cd;
            font-weight: bold;
            color: #856404;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎰 Milli Piyango Çekiliş Sonuçları</h1>
            <p>Super Loto 2026 - {draw_info} - {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
        </div>
        <div class="content">
"""

    if rtp_data:
        rtp_pct = rtp_data["rtp_percentage"]
        category_total = tr_num(rtp_data.get("category_rtp_total", rtp_pct), 2)
        return_per_25 = rtp_data["return_per_25tl"]
        return_per_25_str = tr_num(return_per_25, 2)
        total_prize = tr_num(rtp_data.get("scraped_total_prizes", rtp_data["total_prizes"]), 2)
        devir_prize = tr_num(rtp_data["devir_amount"], 2)
        total_comb = f"{rtp_data['total_combinations']:,}".replace(",", ".")

        html_content += f"""            <div class="rtp-section">
                <div class="rtp-title">📊 Return to Player (RTP) Analizi</div>
                <div class="rtp-grid">
                    <div class="rtp-item">
                        <div class="rtp-label">RTP Oranı</div>
                        <div class="rtp-value">{category_total}%</div>
                        <div class="rtp-subtext">Oyuncuya geri dönüş</div>
                    </div>
                    <div class="rtp-item">
                        <div class="rtp-label">Toplam İkramiye</div>
                        <div class="rtp-value">{total_prize} ₺</div>
                        <div class="rtp-subtext">Devir dahil</div>
                    </div>
                    <div class="rtp-item">
                        <div class="rtp-label">Devir Tutarı</div>
                        <div class="rtp-value">{devir_prize} ₺</div>
                        <div class="rtp-subtext">Sonraki çekilişe</div>
                    </div>
                    <div class="rtp-item">
                        <div class="rtp-label">Olası Kombinasyon</div>
                        <div class="rtp-value">{total_comb}</div>
                        <div class="rtp-subtext">C({TOTAL_NUMBERS}, {SELECTED_NUMBERS})</div>
                    </div>
                    <div class="rtp-item">
                        <div class="rtp-label">Bilet Fiyatı</div>
                        <div class="rtp-value">{rtp_data['ticket_price']} ₺</div>
                    </div>
                    <div class="rtp-item">
                        <div class="rtp-label">25 TL Karşılığı</div>
                        <div class="rtp-value">{return_per_25_str} ₺</div>
                    </div>
                </div>
                <div style="margin-top: 20px; padding: 15px; background: white; border-radius: 8px; font-size: 13px; color: #333; border-left: 4px solid #28a745;">
                    <strong>💡 Açıklama:</strong> Her 25 TL'lik bilet oynadığında, ortalama olarak <strong>{return_per_25_str} TL</strong> geri kazanırsınız.
                </div>
            </div>
"""

    if rtp_data and rtp_data.get("category_analysis"):
        html_content += """            <div class="category-analysis">
                <div class="category-title">📈 Detaylı RTP Analizi</div>
                <table class="category-table">
                    <thead>
                        <tr>
                            <th>Kategori</th>
                            <th>Birim Ödül (₺)</th>
                            <th>Veraset ve İntikal Vergisi (₺)</th>
                            <th>Net Ödül (TL)</th>
                            <th>Olasılık</th>
                            <th>RTP Yüzdesi (%)</th>
                            <th>25 TL Başına Getiri (₺)</th>
                        </tr>
                    </thead>
                    <tbody>
"""

        for tunus in sorted(rtp_data["category_analysis"].keys(), reverse=True):
            cat = rtp_data["category_analysis"][tunus]
            unit_prize_str = tr_num(cat["prize_per_winner"], 2)
            tax_amount = calculate_tax(cat["prize_per_winner"])
            tax_str = tr_num(tax_amount, 2)
            net_prize = cat["prize_per_winner"] - tax_amount
            net_prize_str = tr_num(net_prize, 2)
            probability_value = calculate_probability(tunus)["probability"]

            if probability_value > 0:
                odds_value = 1 / probability_value
                if odds_value == int(odds_value):
                    denominator_str = f"{int(odds_value):,}".replace(",", ".")
                else:
                    denominator_str = f"{odds_value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
                probability_str = f"1/{denominator_str}"
            else:
                probability_str = "N/A"

            rtp_str = tr_num(cat["rtp_percentage"], 4) + "%"
            return_str = tr_num(cat["return_per_25tl"], 4)

            html_content += f"""                        <tr>
                            <td class="tunus">{tunus}</td>
                            <td>{unit_prize_str}</td>
                            <td>{tax_str}</td>
                            <td>{net_prize_str}</td>
                            <td>{probability_str}</td>
                            <td class="highlight-contribution">{rtp_str}</td>
                            <td>{return_str}</td>
                        </tr>
"""

        non_zero_cats = [cat for cat in rtp_data["category_analysis"].values() if cat["prize_per_winner"] > 0]
        total_row_return = sum(cat["return_per_25tl"] for cat in non_zero_cats)
        total_row_rtp_str = tr_num(rtp_data.get("category_rtp_total", rtp_pct), 4) + "%"
        total_row_return_str = tr_num(total_row_return, 4)

        non_zero_cats = [cat for cat in rtp_data["category_analysis"].values() if cat["prize_per_winner"] > 0]
        total_row_return = sum(cat["return_per_25tl"] for cat in non_zero_cats)
        total_row_rtp_str = tr_num(rtp_data.get("category_rtp_total", rtp_pct), 4) + "%"
        total_row_return_str = tr_num(total_row_return, 4)

        html_content += f"""                        <tr class="highlight-contribution">
                            <td><strong>TOPLAM</strong></td>
                            <td><strong>-</strong></td>
                            <td><strong>-</strong></td>
                            <td><strong>-</strong></td>
                            <td><strong>1/1</strong></td>
                            <td><strong>{total_row_rtp_str}</strong></td>
                            <td><strong>{total_row_return_str}</strong></td>
                        </tr>
"""
        html_content += """                    </tbody>
                </table>
            </div>
"""

    if data:
        for section in data:
            html_content += f"""            <div class="winning-section">
                <div class="section-title">Kazanan Numaralar - Liste #{section['list_index']}</div>
                <ul class="items-list">
"""
            for item in section["items"]:
                html_content += f"""                    <li class="list-item">
                        <div class="item-details">
                            <div class="item-row">
                                <span class="label">Tutuş:</span>
                                <span class="value">{item['tunus_sayisi']}</span>
                            </div>
                            <div class="item-row">
                                <span class="label">Kazanan:</span>
                                <span class="value highlight">{item['kazanan_text']}</span>
                                <span class="raw-value">({item['kazanan_sayisi']})</span>
                            </div>
                            <div class="item-row">
                                <span class="label">Ödül:</span>
                                <span class="value">{item['odul_text']}</span>
                            </div>
                        </div>
                    </li>
"""
            html_content += """                </ul>
            </div>
"""
    else:
        html_content += """            <div class="no-data">
                <p>⚠️ Veri alınamadı. Lütfen daha sonra tekrar deneyiniz.</p>
            </div>
"""

    html_content += """        </div>
        <div class="footer">
            <p>Bu sayfa otomatik olarak oluşturulmuştur. Son güncelleme: """ + datetime.now().strftime('%d.%m.%Y %H:%M:%S') + """</p>
        </div>
    </div>
</body>
</html>
"""

    return html_content
