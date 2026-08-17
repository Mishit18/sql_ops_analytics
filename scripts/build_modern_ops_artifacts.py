from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from modern_ops_layer import control_chart_anomalies, dbt_style_quality_checks, seller_sla_action_tiers


def main() -> None:
    outputs = ROOT / "outputs"
    otdr = pd.read_csv(outputs / "otdr.csv")
    seller = pd.read_csv(outputs / "seller.csv")
    anomalies = control_chart_anomalies(otdr, "otdr_pct", "purchase_month")
    tiers = seller_sla_action_tiers(seller)
    checks = dbt_style_quality_checks(
        {
            "otdr": otdr,
            "seller": seller,
            "cohort": pd.read_csv(outputs / "cohort.csv"),
            "corridors": pd.read_csv(outputs / "corridors.csv"),
        }
    )
    anomalies.to_csv(outputs / "control_chart_otdr_anomalies.csv", index=False)
    tiers.to_csv(outputs / "seller_sla_action_tiers.csv", index=False)
    checks.to_csv(outputs / "dbt_style_quality_checks.csv", index=False)
    red_or_amber = int(tiers["action_tier"].isin(["red_suppress", "amber_remediate"]).sum())
    (ROOT / "docs" / "modern_ops_evidence_pack.md").write_text(
        "\n".join(
            [
                "# Modern Ops Evidence Pack",
                "",
                f"- OTDR anomaly periods flagged: {int(anomalies['is_anomaly'].sum())}",
                f"- Sellers assigned remediation/suppression tiers: {red_or_amber}",
                f"- Data quality tables checked: {len(checks)}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
