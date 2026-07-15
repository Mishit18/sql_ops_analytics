# Interactive Dashboard

The dashboard is a Streamlit app built on the committed KPI outputs. It is designed for quick local exploration without requiring the raw Kaggle CSV files.

Run from the project root:

```bash
streamlit run dashboard/app.py
```

The app includes:

- executive KPI cards
- OTDR and GMV trend views
- seller scorecard exploration
- geographic SLA ranking
- cohort retention matrix
- freight corridor analysis
- product velocity table

## Review Flow

1. Start on the Executive tab to check overall OTDR, worst operational month, seller concentration, and retention.
2. Move to Sellers to inspect which sellers combine high late rates with weak review scores.
3. Use Geography to compare state-level SLA breach rates and identify long-haul delivery risk.
4. Use Retention to review cohort decay after first purchase.
5. Use Freight to prioritize routes where cost and lateness are both elevated.

## Inputs

The app reads from `outputs/*.csv` and `outputs/*.png`. Rebuild those artifacts with:

```bash
python build_project.py
```

This makes the dashboard lightweight for reviewers while preserving full reproducibility from the raw dataset.
