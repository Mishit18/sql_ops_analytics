# Executive Brief

## Project Objective

Build a SQL-first operations analytics pipeline for Olist e-commerce orders, then use the resulting KPIs to identify delivery reliability, seller performance, customer retention, and freight efficiency opportunities.

## Dataset

- 8 operational source tables
- 96,470 delivered orders in the cleaned analytical view
- Purchase coverage from 2016-09-04 to 2018-10-17
- 97.01% of raw orders retained after delivered-order cleaning rules

## Headline KPIs

| KPI | Result |
|---|---:|
| Overall OTDR | 91.89% |
| Operational-month OTDR range | 78.64% to 98.87% |
| Bottom-decile seller breach share | 17.0% |
| Bottom-decile seller order share | 8.4% |
| Month-1 retention | 0.47% |
| Month-3 retention | 0.25% |
| Average order value | BRL 160 |
| Total GMV analyzed | BRL 15.4M |

## Decisions Supported

1. Vendor tiering: rank sellers using a composite score that combines delivery reliability and review quality.
2. Lane-level SLA redesign: test revised carrier coverage or promise windows on high-risk state/category lanes.
3. Repeat-order intervention: launch post-delivery re-engagement and second-purchase freight incentives.
4. Freight corridor management: prioritize SP -> MA and similar lanes for consolidation or carrier renegotiation.

## Interactive Review

The Streamlit dashboard turns the static analysis into a filterable operations control room. Reviewers can adjust seller order thresholds, filter customer states, inspect category lead-time patterns, compare seller outliers, and prioritize freight corridors without rerunning the full build.

## Quantified Recommendations

- Reduce late deliveries among bottom-decile sellers by 25%, preventing about 333 late deliveries over the observed period.
- Reduce AL state breaches by 20%, avoiding about 19 late orders tied to roughly BRL 63,451 of GMV exposure.
- Lift month-3 retention by 0.5 percentage points, creating an estimated 481 incremental repeat orders.

## Portfolio Positioning

This project is designed for Strategy & Operations, Marketplace Operations, Supply Chain Analytics, and Business Operations roles. It emphasizes production SQL habits, metric grain discipline, business recommendation quality, and dashboard-ready analytical storytelling.
