from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"


st.set_page_config(
    page_title="Olist Operations Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def read_csv(name: str, parse_dates: list[str] | None = None) -> pd.DataFrame:
    return pd.read_csv(OUTPUT_DIR / name, parse_dates=parse_dates)


@st.cache_data
def metrics() -> dict[str, str]:
    frame = read_csv("kpi_summary.csv")
    return dict(zip(frame["metric"], frame["value"]))


def metric_value(values: dict[str, str], key: str, suffix: str = "", decimals: int = 1) -> str:
    value = values[key]
    try:
        number = float(value)
    except ValueError:
        return value
    return f"{number:,.{decimals}f}{suffix}"


def show_png(name: str, caption: str) -> None:
    st.image(str(OUTPUT_DIR / name), caption=caption, use_container_width=True)


values = metrics()
otdr = read_csv("otdr.csv", parse_dates=["purchase_month"])
seller = read_csv("seller.csv")
sla_state = read_csv("sla_state.csv")
lead_category = read_csv("lead_category.csv")
velocity = read_csv("velocity.csv")
freight = read_csv("freight.csv")
corridors = read_csv("corridors.csv")
cohort = read_csv("cohort.csv", parse_dates=["cohort_month"])
volume = read_csv("volume.csv", parse_dates=["purchase_week"])


st.title("Olist Operations Analytics")
st.caption("SQL-first supply chain, marketplace, and customer operations dashboard")

with st.sidebar:
    st.header("Filters")
    min_orders = st.slider("Minimum seller orders", 30, int(seller["total_orders"].max()), 30, step=10)
    selected_states = st.multiselect(
        "Customer states",
        sorted(sla_state["customer_state"].unique()),
        default=sorted(sla_state["customer_state"].unique()),
    )
    selected_categories = st.multiselect(
        "Product categories",
        sorted(lead_category["category_en"].dropna().unique()),
        default=list(lead_category.sort_values("total_orders", ascending=False).head(10)["category_en"]),
    )


filtered_sellers = seller[seller["total_orders"] >= min_orders].copy()
filtered_states = sla_state[sla_state["customer_state"].isin(selected_states)].copy()
filtered_categories = lead_category[lead_category["category_en"].isin(selected_categories)].copy()

metric_cols = st.columns(5)
metric_cols[0].metric("Delivered orders", f"{float(values['total_orders']):,.0f}")
metric_cols[1].metric("Overall OTDR", metric_value(values, "overall_otdr_pct", "%", 2))
metric_cols[2].metric("Worst OTDR month", f"{values['worst_otdr_month']} ({float(values['worst_otdr_pct']):.1f}%)")
metric_cols[3].metric("Bottom seller breach share", metric_value(values, "bottom_seller_breach_share_pct", "%", 1))
metric_cols[4].metric("Month-3 retention", metric_value(values, "retention_m3_pct", "%", 2))

tab_overview, tab_sellers, tab_geo, tab_customer, tab_freight = st.tabs(
    ["Executive", "Sellers", "Geography", "Retention", "Freight"]
)

with tab_overview:
    left, right = st.columns([1.15, 0.85])
    with left:
        show_png("plot_01_otdr_trend.png", "Monthly OTDR with rolling average and confidence interval")
    with right:
        st.subheader("Operational readout")
        st.write(
            "The pipeline isolates delivered-order performance and separates raw KPI tables from narrative reporting thresholds. "
            "The key operational issue is not only average delivery reliability, but concentration of reliability risk by seller and lane."
        )
        st.dataframe(
            filtered_categories[
                ["category_en", "total_orders", "avg_lead_time", "p90_lead_time", "late_rate_pct"]
            ].sort_values("p90_lead_time", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
    show_png("plot_06_gmv_orders_dual_axis.png", "Weekly GMV and order volume")

with tab_sellers:
    left, right = st.columns([1.1, 0.9])
    with left:
        show_png("plot_03_seller_scorecard_scatter.png", "Seller late rate vs review score")
    with right:
        st.subheader("Worst sellers by composite score")
        st.dataframe(
            filtered_sellers[
                [
                    "seller_id",
                    "seller_state",
                    "total_orders",
                    "late_rate_pct",
                    "avg_review_score",
                    "seller_composite_score",
                ]
            ]
            .sort_values("seller_composite_score")
            .head(20),
            use_container_width=True,
            hide_index=True,
        )
    show_png("plot_10_seller_score_distribution.png", "Seller score distribution with bottom decile")

with tab_geo:
    left, right = st.columns([1, 1])
    with left:
        show_png("plot_04_sla_breach_choropleth.png", "State-level SLA breach rate")
    with right:
        st.subheader("State SLA ranking")
        st.dataframe(
            filtered_states[
                ["customer_state", "total_orders", "breach_rate_pct", "avg_lead_time", "avg_delay_when_late"]
            ].sort_values("breach_rate_pct", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
    show_png("plot_09_p90_lead_time_category.png", "P90 lead time by category")

with tab_customer:
    left, right = st.columns([1.1, 0.9])
    with left:
        show_png("plot_05_cohort_retention_heatmap.png", "Customer cohort retention")
    with right:
        st.subheader("Retention table")
        retention_matrix = cohort.pivot(index="cohort_month", columns="month_number", values="retention_rate_pct")
        retention_matrix.index = retention_matrix.index.strftime("%Y-%m")
        st.dataframe(retention_matrix, use_container_width=True)
        st.write(
            "Retention is structurally low after the first purchase, making second-purchase timing and post-delivery engagement the highest-leverage customer operations lever."
        )

with tab_freight:
    left, right = st.columns([1, 1])
    with left:
        show_png("plot_07_freight_efficiency_scatter.png", "Freight cost vs lead time by lane/category")
    with right:
        st.subheader("Worst corridors")
        st.dataframe(
            corridors[
                ["seller_state", "customer_state", "shipments", "avg_freight_cost", "late_rate_pct", "avg_lead_time"]
            ].head(20),
            use_container_width=True,
            hide_index=True,
        )
    st.subheader("Product velocity")
    st.dataframe(
        velocity[["category_en", "units_sold", "units_per_week", "avg_lead_time", "stockout_risk"]]
        .sort_values("units_per_week", ascending=False)
        .head(30),
        use_container_width=True,
        hide_index=True,
    )
