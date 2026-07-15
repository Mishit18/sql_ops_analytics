# Resume Notes

## Short Project Title

SQL Operations Analytics Pipeline for E-Commerce Supply Chain Performance

## Resume Bullets

- Built SQL analytics pipeline on 96,470 e-commerce orders across 8 DuckDB tables; computed 8 supply-chain KPIs including OTDR 91.9%, P90 lead time, and cohort retention.
- Identified bottom-10% sellers driving 17.0% of SLA breaches; proposed composite vendor scorecard using delivery reliability and review quality for tiering.
- Computed customer cohort retention: month-1 0.47%, month-3 0.25%, month-6 0.26%; segmented by acquisition cohort and quantified repeat-order gap.
- Diagnosed SP -> MA as highest-risk corridor, with freight cost 98% above median and 23.9% late rate; recommended carrier consolidation to reduce cost by estimated 8-12%.

## Interview Talking Points

- Explained why KPI grain matters and avoided double-counting multi-item orders in category and seller metrics.
- Used DuckDB as an analytical warehouse layer rather than doing KPI logic only in Pandas.
- Converted operational signals into interventions: seller tiering, carrier coverage tests, SLA redesign, and retention triggers.
- Treated low-volume months carefully by separating raw KPI tables from narrative reporting thresholds.
- Added a Streamlit dashboard and automated validation suite so the project can be reviewed interactively and checked reproducibly.

## Skills Demonstrated

- SQL analytics engineering
- DuckDB
- Data quality validation
- KPI design
- Supply chain analytics
- Marketplace operations
- Cohort retention analysis
- Dashboarding with Python
- Operational recommendation sizing
