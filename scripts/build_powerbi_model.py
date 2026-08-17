from __future__ import annotations

import json
from pathlib import Path

import duckdb
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "olist_ops.duckdb"
BI_DATA = ROOT / "bi" / "data"
OUTPUTS = ROOT / "outputs"


EXPORTS = {
    "fact_orders": """
        WITH review_per_order AS (
            SELECT order_id, AVG(review_score) AS review_score
            FROM reviews
            GROUP BY order_id
        )
        SELECT
            o.order_id,
            o.customer_unique_id AS customer_id,
            CAST(strftime(o.purchase_ts, '%Y%m%d') AS INTEGER) AS date_key,
            o.order_status,
            o.actual_lead_time_days,
            o.promised_lead_time_days,
            o.delay_days,
            o.is_late,
            o.is_undelivered,
            r.review_score
        FROM orders_clean o
        LEFT JOIN review_per_order r USING (order_id)
    """,
    "fact_order_items": """
        SELECT
            i.order_id,
            i.order_item_id,
            i.product_id,
            i.seller_id,
            i.price,
            i.freight_value
        FROM items i
        INNER JOIN orders_clean o USING (order_id)
    """,
    "dim_customers": """
        SELECT DISTINCT
            customer_unique_id AS customer_id,
            customer_city,
            customer_state
        FROM customers
    """,
    "dim_sellers": """
        SELECT DISTINCT seller_id, seller_city, seller_state
        FROM sellers
    """,
    "dim_products": """
        SELECT DISTINCT
            p.product_id,
            COALESCE(t.product_category_name_english, p.product_category_name, 'Unknown') AS category,
            p.product_weight_g,
            p.product_length_cm,
            p.product_height_cm,
            p.product_width_cm
        FROM products p
        LEFT JOIN translations t USING (product_category_name)
    """,
    "dim_dates": """
        WITH bounds AS (
            SELECT MIN(CAST(purchase_ts AS DATE)) AS min_date,
                   MAX(CAST(purchase_ts AS DATE)) AS max_date
            FROM orders_clean
        )
        SELECT
            CAST(strftime(d, '%Y%m%d') AS INTEGER) AS date_key,
            d AS full_date,
            year(d) AS year,
            quarter(d) AS quarter,
            month(d) AS month_number,
            strftime(d, '%B') AS month_name,
            week(d) AS week_number,
            dayofweek(d) AS day_of_week
        FROM bounds,
             generate_series(min_date, max_date, INTERVAL 1 DAY) AS dates(d)
    """,
}


def _quality_checks(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    orders = frames["fact_orders"]
    items = frames["fact_order_items"]
    checks = [
        ("fact_orders_order_id_unique", orders["order_id"].is_unique),
        ("fact_orders_order_id_not_null", orders["order_id"].notna().all()),
        ("fact_items_composite_key_unique", not items.duplicated(["order_id", "order_item_id"]).any()),
        ("fact_items_order_fk_valid", items["order_id"].isin(orders["order_id"]).all()),
        ("late_flag_binary", orders["is_late"].dropna().isin([0, 1]).all()),
        ("nonnegative_price", items["price"].dropna().ge(0).all()),
        ("nonnegative_freight", items["freight_value"].dropna().ge(0).all()),
    ]
    return pd.DataFrame(
        [{"check": name, "status": "pass" if passed else "fail"} for name, passed in checks]
    )


def build() -> dict[str, object]:
    if not DATABASE.exists():
        raise FileNotFoundError("Run `python build_project.py` before exporting the BI model.")

    BI_DATA.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(exist_ok=True)
    connection = duckdb.connect(str(DATABASE), read_only=True)
    frames = {name: connection.execute(sql).df() for name, sql in EXPORTS.items()}
    connection.close()

    for name, frame in frames.items():
        frame.to_csv(BI_DATA / f"{name}.csv", index=False)

    checks = _quality_checks(frames)
    checks.to_csv(OUTPUTS / "powerbi_refresh_checks.csv", index=False)
    if not checks["status"].eq("pass").all():
        raise ValueError("Power BI export failed one or more data-quality checks.")

    manifest = {
        "source": "Olist Brazilian E-Commerce public dataset",
        "model": "Power BI-ready star schema",
        "grain": {
            "fact_orders": "one row per delivered or operational order",
            "fact_order_items": "one row per order item",
        },
        "rows": {name: int(len(frame)) for name, frame in frames.items()},
        "quality_checks_passed": int(checks["status"].eq("pass").sum()),
        "quality_checks_total": int(len(checks)),
    }
    (OUTPUTS / "powerbi_model_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
