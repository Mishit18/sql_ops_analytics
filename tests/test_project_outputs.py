from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"


def read_output(name: str) -> pd.DataFrame:
    return pd.read_csv(OUTPUT_DIR / name)


def test_kpi_summary_matches_output_tables() -> None:
    summary = dict(zip(read_output("kpi_summary.csv")["metric"], read_output("kpi_summary.csv")["value"]))
    otdr = read_output("otdr.csv")
    total_orders = otdr["total_orders"].sum()
    late_orders = otdr["late_orders"].sum()
    expected_otdr = round(100 * (total_orders - late_orders) / total_orders, 2)

    assert int(float(summary["total_orders"])) == int(total_orders)
    assert float(summary["overall_otdr_pct"]) == expected_otdr
    assert int(float(summary["otdr_reporting_month_threshold"])) == 100


def test_cohort_month_zero_is_full_retention() -> None:
    cohort = read_output("cohort.csv")
    month_zero = cohort[cohort["month_number"] == 0]

    assert not month_zero.empty
    assert (month_zero["retention_rate_pct"] == 100.0).all()
    assert (month_zero["active_customers"] == month_zero["cohort_customers"]).all()


def test_bottom_seller_breach_concentration_is_material() -> None:
    summary = dict(zip(read_output("kpi_summary.csv")["metric"], read_output("kpi_summary.csv")["value"]))
    breach_share = float(summary["bottom_seller_breach_share_pct"])
    order_share = float(summary["bottom_seller_order_share_pct"])

    assert breach_share > order_share
    assert breach_share >= 15.0


def test_state_breach_rates_are_valid_percentages() -> None:
    states = read_output("sla_state.csv")

    assert states["customer_state"].nunique() == len(states)
    assert states["breach_rate_pct"].between(0, 100).all()
    assert states["total_orders"].sum() >= 90_000


def test_dashboard_dependencies_exist() -> None:
    assert (ROOT / "dashboard" / "app.py").exists()
    assert (ROOT / "dashboard" / "README.md").exists()
    for plot in [
        "plot_01_otdr_trend.png",
        "plot_03_seller_scorecard_scatter.png",
        "plot_04_sla_breach_choropleth.png",
        "plot_05_cohort_retention_heatmap.png",
    ]:
        assert (OUTPUT_DIR / plot).stat().st_size > 10_000
