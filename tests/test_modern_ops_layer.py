from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "scripts"))

from modern_ops_layer import control_chart_anomalies, dbt_style_quality_checks, seller_sla_action_tiers


def test_control_chart_anomalies_flags_spikes():
    frame = pd.DataFrame({"month": range(8), "late_rate_pct": [5, 6, 5, 6, 5, 6, 5, 30]})
    out = control_chart_anomalies(frame, "late_rate_pct", "month", z_threshold=2.0)

    assert out["is_anomaly"].sum() == 1
    assert out.iloc[-1]["is_anomaly"]


def test_dbt_style_quality_checks_reports_status():
    checks = dbt_style_quality_checks({"orders": pd.DataFrame({"a": [1, 2], "b": [3, 4]})})

    assert checks.iloc[0]["status"] == "pass"
    assert checks.iloc[0]["rows"] == 2


def test_seller_sla_action_tiers_creates_operating_actions():
    seller = pd.DataFrame(
        {
            "seller_id": ["a", "b", "c", "d", "e"],
            "late_rate_pct": [2, 4, 7, 12, 30],
            "seller_composite_score": [90, 75, 60, 45, 10],
            "total_orders": [100, 100, 100, 100, 100],
        }
    )
    out = seller_sla_action_tiers(seller)

    assert "action_tier" in out.columns
    assert set(out["action_tier"]).issubset({"green_monitor", "amber_remediate", "red_suppress"})

