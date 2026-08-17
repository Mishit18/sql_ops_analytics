# Power BI Delivery Pack

This folder converts the real Olist analytics warehouse into a recruiter-reviewable BI specification. It deliberately does not include a fabricated `.pbix`: Power BI Desktop must create that binary artifact.

## Build the semantic layer

```bash
python build_project.py
python scripts/build_powerbi_model.py
```

The export creates two fact tables and four dimensions under `bi/data/`, then writes refresh evidence to:

- `outputs/powerbi_model_manifest.json`
- `outputs/powerbi_refresh_checks.csv`

## Model relationships

| From | Cardinality | To | Filter direction |
|---|---:|---|---|
| `DimDates[date_key]` | 1:* | `FactOrders[date_key]` | Single |
| `DimCustomers[customer_id]` | 1:* | `FactOrders[customer_id]` | Single |
| `FactOrders[order_id]` | 1:* | `FactOrderItems[order_id]` | Single |
| `DimProducts[product_id]` | 1:* | `FactOrderItems[product_id]` | Single |
| `DimSellers[seller_id]` | 1:* | `FactOrderItems[seller_id]` | Single |

Use explicit one-to-many relationships and avoid bidirectional filters. Mark `DimDates[full_date]` as the date table.

## Report pages

1. **Executive Operations:** orders, GMV, OTDR, SLA breach rate, P90 lead time and month-over-month change.
2. **Seller Reliability:** seller score distribution, breach concentration, GMV exposure and remediation tier.
3. **Freight and Geography:** seller-state/customer-state lanes, freight-to-GMV ratio and late-delivery risk.
4. **Customer Retention:** acquisition cohorts, repeat orders, category mix and post-delivery experience.
5. **Data Quality:** refresh timestamp, row counts, key uniqueness, referential integrity and failed checks.

Copy the measures from `measures.dax`, format rates as percentages, and use drill-through from seller and state views to order-level evidence.

## Power BI Desktop validation

The semantic model was opened and queried in Power BI Desktop on 18 August 2026. Power BI recognized all 17 DAX measures and returned 96,470 orders, 91.89% OTDR, 8.11% SLA breach rate, BRL 13.22M GMV, and BRL 2.20M freight cost. The aggregate validation record is committed at `outputs/powerbi_desktop_validation.json`.

Defensible resume wording: **Built a Power BI semantic model with 17 DAX measures; validated OTDR, SLA, GMV, and freight KPIs.** This repository does not claim a deployed Power BI Service dashboard.
