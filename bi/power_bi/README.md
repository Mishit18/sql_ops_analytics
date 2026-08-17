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

## Defensible resume wording

Until a report is opened and verified in Power BI Desktop, describe this artifact as a **Power BI-ready star schema and DAX measure pack**, not as a deployed Power BI dashboard.
