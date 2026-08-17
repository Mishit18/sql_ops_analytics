# External Review Packet

## Claims to verify

- 96,470 operational orders analyzed from the public Olist dataset.
- DuckDB model spans eight source tables and standalone KPI queries.
- Bottom-decile sellers contribute 17.0% of SLA breaches from 8.4% of scored seller orders.
- Power BI-ready export contains 96,470 order rows and 110,189 item rows; all seven refresh checks pass.

## Reproduce

```bash
python build_project.py
python scripts/build_powerbi_model.py
python scripts/build_public_evidence_site.py
python -m pytest -q
```

## Evidence

- `outputs/kpi_summary.csv`
- `outputs/powerbi_model_manifest.json`
- `outputs/powerbi_refresh_checks.csv`
- `bi/power_bi/measures.dax`
- `site/index.html`
- `docs/methodology.md`

## Reviewer checklist

- Confirm grains and joins do not double-count orders.
- Recompute OTDR and seller concentration from exported tables.
- Review DAX denominator choices and relationship directions.
- Confirm recommendations are framed as proposals, not measured interventions.
- Record reviewer name, role, date, and only the claims personally checked.
