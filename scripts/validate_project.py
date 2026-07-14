from __future__ import annotations

import csv
import re
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SQL = [
    "00_setup_and_clean.sql",
    "01_kpi_otdr_monthly.sql",
    "02_kpi_lead_time_category.sql",
    "03_kpi_seller_scorecard.sql",
    "04_kpi_sla_breach_geo.sql",
    "05_kpi_cohort_retention.sql",
    "06_kpi_volume_trend.sql",
    "07_kpi_product_velocity.sql",
    "08_kpi_freight_efficiency.sql",
]

REQUIRED_PLOTS = [
    "plot_01_otdr_trend.png",
    "plot_02_lead_time_violin.png",
    "plot_03_seller_scorecard_scatter.png",
    "plot_04_sla_breach_choropleth.png",
    "plot_05_cohort_retention_heatmap.png",
    "plot_06_gmv_orders_dual_axis.png",
    "plot_07_freight_efficiency_scatter.png",
    "plot_08_product_velocity.png",
    "plot_09_p90_lead_time_category.png",
    "plot_10_seller_score_distribution.png",
]

REQUIRED_OUTPUTS = [
    "kpi_summary.csv",
    "schema_validation.txt",
    "otdr.csv",
    "lead_category.csv",
    "seller.csv",
    "sla_state.csv",
    "cohort.csv",
    "volume.csv",
    "velocity.csv",
    "freight.csv",
    "corridors.csv",
]

FORBIDDEN_TERMS = [
    "Co" + "dex",
    "Chat" + "GPT",
    "Open" + "AI",
    "assi" + "stant",
    "AI-" + "generated",
    "generated " + "by",
    "TO" + "DO",
    "place" + "holder",
    "[" + "X" + "]",
    "[" + "Y" + "]",
    "[" + "Z" + "]",
]
FORBIDDEN_TEXT = re.compile("|".join(re.escape(term) for term in FORBIDDEN_TERMS), re.IGNORECASE)


def require_file(path: Path, min_bytes: int = 1) -> None:
    if not path.exists():
        raise AssertionError(f"Missing required file: {path.relative_to(ROOT)}")
    if path.is_file() and path.stat().st_size < min_bytes:
        raise AssertionError(f"File is unexpectedly small: {path.relative_to(ROOT)}")


def validate_text_files() -> None:
    for relative in ["README.md", "summary.md", "docs/methodology.md", "docs/executive_brief.md"]:
        path = ROOT / relative
        require_file(path)
        text = path.read_text(encoding="utf-8")
        match = FORBIDDEN_TEXT.search(text)
        if match:
            raise AssertionError(f"Forbidden repository text in {relative}: {match.group(0)}")


def validate_sql_files() -> None:
    for name in REQUIRED_SQL:
        path = ROOT / "queries" / name
        require_file(path, min_bytes=100)
        text = path.read_text(encoding="utf-8").lower()
        if "create or replace" not in text:
            raise AssertionError(f"SQL file does not create a reproducible object: {name}")


def validate_outputs() -> None:
    for name in REQUIRED_OUTPUTS:
        require_file(ROOT / "outputs" / name, min_bytes=50)
    for name in REQUIRED_PLOTS:
        require_file(ROOT / "outputs" / name, min_bytes=10_000)

    with (ROOT / "outputs" / "kpi_summary.csv").open(newline="", encoding="utf-8") as handle:
        rows = {row["metric"]: row["value"] for row in csv.DictReader(handle)}

    expected = {
        "overall_otdr_pct",
        "bottom_seller_breach_share_pct",
        "retention_m1_pct",
        "retention_m3_pct",
        "total_orders",
        "total_gmv",
    }
    missing = expected.difference(rows)
    if missing:
        raise AssertionError(f"kpi_summary.csv missing metrics: {sorted(missing)}")
    if float(rows["total_orders"]) < 90_000:
        raise AssertionError("Delivered order count fell below quality threshold")


def validate_notebook() -> None:
    path = ROOT / "sql_ops_analytics.ipynb"
    require_file(path, min_bytes=1_000)
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    if len(notebook.cells) < 20:
        raise AssertionError("Notebook should contain narrative and SQL appendix cells")


def main() -> None:
    validate_text_files()
    validate_sql_files()
    validate_outputs()
    validate_notebook()
    print("Project validation passed.")


if __name__ == "__main__":
    main()
