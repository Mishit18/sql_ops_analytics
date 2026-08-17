from __future__ import annotations

import pandas as pd


def control_chart_anomalies(
    frame: pd.DataFrame,
    metric_col: str,
    date_col: str,
    z_threshold: float = 2.5,
) -> pd.DataFrame:
    required = {metric_col, date_col}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    work = frame[[date_col, metric_col]].dropna().copy()
    mean = work[metric_col].mean()
    std = work[metric_col].std(ddof=0)
    if std == 0 or pd.isna(std):
        work["z_score"] = 0.0
    else:
        work["z_score"] = (work[metric_col] - mean) / std
    work["is_anomaly"] = work["z_score"].abs() >= z_threshold
    return work.sort_values(date_col)


def dbt_style_quality_checks(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for name, table in tables.items():
        rows.append(
            {
                "table": name,
                "rows": int(len(table)),
                "columns": int(len(table.columns)),
                "duplicate_rows": int(table.duplicated().sum()),
                "null_cells": int(table.isna().sum().sum()),
                "status": "pass" if len(table) > 0 and table.duplicated().sum() == 0 else "review",
            }
        )
    return pd.DataFrame(rows)


def seller_sla_action_tiers(seller: pd.DataFrame) -> pd.DataFrame:
    required = {"seller_id", "late_rate_pct", "seller_composite_score", "total_orders"}
    missing = required - set(seller.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    out = seller.copy()
    low_score = out["seller_composite_score"].quantile(0.10)
    high_late = out["late_rate_pct"].quantile(0.80)
    out["action_tier"] = "green_monitor"
    out.loc[(out["seller_composite_score"] <= low_score) | (out["late_rate_pct"] >= high_late), "action_tier"] = "amber_remediate"
    out.loc[(out["seller_composite_score"] <= low_score) & (out["late_rate_pct"] >= high_late), "action_tier"] = "red_suppress"
    return out.sort_values(["action_tier", "late_rate_pct"], ascending=[False, False])

