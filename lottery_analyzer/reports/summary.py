from datetime import datetime
from html import escape
import os
from pathlib import Path

from lottery_analyzer.models import GameRunResult
from lottery_analyzer.shared.formatting import tr_num


def _rtp_value(result):
    analysis = result.analysis
    return analysis.get("category_rtp_total", analysis.get("rtp_percentage", 0))


def _expected_return(result):
    analysis = result.analysis
    return analysis.get("return_per_ticket", analysis.get("return_per_25tl", 0))


def generate_summary_html(results, output_path):
    ranked_results = sorted(results, key=_rtp_value, reverse=True)
    rows = []

    for rank, result in enumerate(ranked_results, start=1):
        game_name = escape(result.game.name)
        report_link = escape(
            Path(os.path.relpath(result.report_path, output_path.parent)).as_posix(),
            quote=True,
        )
        rtp_text = tr_num(_rtp_value(result), 2)
        ticket_price_text = tr_num(result.game.ticket_price, 2)
        expected_return_text = tr_num(_expected_return(result), 2)
        rows.append(
            f"""                <tr>
                    <td class="rank">{rank}</td>
                    <th scope="row">{game_name}</th>
                    <td class="numeric">{rtp_text}%</td>
                    <td class="numeric">{ticket_price_text} TL</td>
                    <td class="numeric">{expected_return_text} TL</td>
                    <td><a class="report-link" href="{report_link}">Raporu aç</a></td>
                </tr>"""
        )

    rows_html = "\n".join(rows)
    generated_at = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Milli Piyango Oyun Analizleri</title>
    <style>
        :root {{ color-scheme: light; font-family: 'Segoe UI', Tahoma, sans-serif; color: #202a32; background: #f3f6f7; }}
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; padding: 32px 18px; }}
        main {{ width: min(100%, 980px); margin: 0 auto; }}
        header {{ border-bottom: 3px solid #177e78; padding: 8px 0 18px; margin-bottom: 24px; }}
        h1 {{ margin: 0 0 8px; font-size: 26px; }}
        .meta {{ color: #59666f; font-size: 13px; }}
        .table-wrap {{ overflow-x: auto; background: #fff; border: 1px solid #d9e0e2; border-radius: 6px; }}
        table {{ width: 100%; border-collapse: collapse; min-width: 700px; }}
        th, td {{ text-align: left; padding: 14px 16px; border-bottom: 1px solid #e4e9ea; }}
        thead th {{ background: #eaf3f2; color: #244946; font-size: 12px; }}
        tbody tr:last-child th, tbody tr:last-child td {{ border-bottom: 0; }}
        .rank {{ width: 56px; color: #69767c; }}
        .numeric {{ text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }}
        .report-link {{ display: inline-block; padding: 8px 12px; border-radius: 4px; background: #177e78; color: #fff; text-decoration: none; white-space: nowrap; }}
        .report-link:hover {{ background: #116861; }}
        .empty {{ padding: 28px; color: #59666f; }}
        footer {{ margin-top: 16px; color: #69767c; font-size: 12px; }}
        @media (max-width: 640px) {{ body {{ padding: 20px 10px; }} h1 {{ font-size: 22px; }} th, td {{ padding: 11px 12px; }} }}
    </style>
</head>
<body>
    <main>
        <header>
            <h1>Milli Piyango Oyun Analizleri</h1>
            <div class="meta">RTP oranına göre yüksekten düşüğe sıralanmıştır.</div>
        </header>
        <div class="table-wrap">
            <table>
                <thead>
                    <tr><th>Sıra</th><th>Oyun</th><th class="numeric">RTP</th><th class="numeric">Kolon ücreti</th><th class="numeric">Kolon başına beklenen getiri</th><th>Detay</th></tr>
                </thead>
                <tbody>
                    {rows_html if rows_html else '<tr><td class="empty" colspan="6">Henüz rapor üretilemedi.</td></tr>'}
                </tbody>
            </table>
        </div>
        <footer>Oluşturulma zamanı: {generated_at}</footer>
    </main>
</body>
</html>
"""
