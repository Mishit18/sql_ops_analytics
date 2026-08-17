from __future__ import annotations

from pathlib import Path
from shutil import copy2

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
SITE = ROOT / "site"
ASSETS = SITE / "assets"


def metric(summary: dict[str, str], key: str, suffix: str = "") -> str:
    value = float(summary[key])
    if value.is_integer():
        return f"{int(value):,}{suffix}"
    return f"{value:,.2f}{suffix}"


def build() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    summary_frame = pd.read_csv(OUTPUTS / "kpi_summary.csv")
    summary = dict(zip(summary_frame["metric"], summary_frame["value"].astype(str)))

    plots = {
        "otdr.png": "plot_01_otdr_trend.png",
        "sellers.png": "plot_03_seller_scorecard_scatter.png",
        "geography.png": "plot_04_sla_breach_choropleth.png",
        "retention.png": "plot_05_cohort_retention_heatmap.png",
    }
    for destination, source in plots.items():
        copy2(OUTPUTS / source, ASSETS / destination)

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Olist Operations Analytics</title>
  <style>
    :root {{ --ink:#17212b; --muted:#5b6672; --line:#d8dee5; --accent:#176b87; --warn:#b64b3d; --bg:#f5f7f9; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Arial, sans-serif; color:var(--ink); background:var(--bg); }}
    header {{ background:#fff; border-bottom:1px solid var(--line); padding:28px max(24px,5vw) 22px; }}
    h1 {{ margin:0 0 8px; font-size:30px; letter-spacing:0; }}
    header p {{ margin:0; color:var(--muted); max-width:880px; line-height:1.5; }}
    main {{ max-width:1200px; margin:0 auto; padding:24px; }}
    .kpis {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; margin-bottom:18px; }}
    .kpi {{ background:#fff; border:1px solid var(--line); padding:16px; border-radius:6px; }}
    .kpi span {{ display:block; color:var(--muted); font-size:13px; margin-bottom:8px; }}
    .kpi strong {{ font-size:25px; }}
    .charts {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; }}
    figure {{ margin:0; background:#fff; border:1px solid var(--line); padding:14px; border-radius:6px; }}
    figure img {{ width:100%; height:auto; display:block; }}
    figcaption {{ font-weight:700; margin:4px 0 10px; }}
    section {{ background:#fff; border:1px solid var(--line); border-radius:6px; padding:18px; margin-top:18px; }}
    li {{ margin:8px 0; line-height:1.45; }}
    a {{ color:var(--accent); }}
    footer {{ color:var(--muted); font-size:13px; margin:20px 0; line-height:1.5; }}
    @media (max-width:800px) {{ .kpis,.charts {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
  <header>
    <h1>Olist Operations Analytics</h1>
    <p>SQL-first service, seller, freight, and retention analysis on the public Olist Brazilian E-Commerce dataset. Figures are reproducible from DuckDB views and validated output tables.</p>
  </header>
  <main>
    <div class="kpis">
      <div class="kpi"><span>Delivered orders</span><strong>{metric(summary, 'total_orders')}</strong></div>
      <div class="kpi"><span>Overall OTDR</span><strong>{metric(summary, 'overall_otdr_pct', '%')}</strong></div>
      <div class="kpi"><span>Bottom-decile breach share</span><strong>{metric(summary, 'bottom_seller_breach_share_pct', '%')}</strong></div>
      <div class="kpi"><span>Bottom-decile order share</span><strong>{metric(summary, 'bottom_seller_order_share_pct', '%')}</strong></div>
    </div>
    <div class="charts">
      <figure><figcaption>On-time delivery trend</figcaption><img src="assets/otdr.png" alt="Monthly on-time delivery trend"></figure>
      <figure><figcaption>Seller reliability</figcaption><img src="assets/sellers.png" alt="Seller reliability scorecard"></figure>
      <figure><figcaption>Geographic SLA risk</figcaption><img src="assets/geography.png" alt="Geographic SLA breach analysis"></figure>
      <figure><figcaption>Customer retention</figcaption><img src="assets/retention.png" alt="Customer cohort retention heatmap"></figure>
    </div>
    <section>
      <h2>Decision summary</h2>
      <ul>
        <li>Prioritize bottom-decile sellers for remediation because their breach share materially exceeds their order share.</li>
        <li>Use lane-level SLA policies for high-risk seller-state/customer-state corridors instead of one national promise.</li>
        <li>Target the sharp post-purchase retention loss with delivery-triggered re-engagement and freight experiments.</li>
        <li>Track OTDR, P90 lead time, seller tier, freight-to-GMV, and refresh checks in the weekly operating review.</li>
      </ul>
    </section>
    <footer>
      Source: public Olist dataset. This is an analytical case study, not company production reporting.
      Reproduce it from the <a href="https://github.com/Mishit18/sql_ops_analytics">project repository</a>.
    </footer>
  </main>
</body>
</html>
"""
    (SITE / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    build()
