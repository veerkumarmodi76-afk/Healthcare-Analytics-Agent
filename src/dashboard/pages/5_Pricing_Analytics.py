"""
5_Pricing_Analytics.py

Pricing Analytics Dashboard

Responsibilities
----------------
- Premium Quotes
- Premium Summary
- Pricing Report
- Premium Leakage
- Pricing Insights

Presentation layer only.
No pricing logic lives here.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.utils.dashboard_loader import DashboardLoader

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Pricing Analytics",
    page_icon="💰",
    layout="wide",
)

loader = DashboardLoader()

# ==========================================================
# Portfolio Validation
# ==========================================================

if not loader.portfolio_exists():

    st.warning(
        """
No processed portfolio found.

Please execute the Healthcare Analytics Pipeline first.
"""
    )
    st.stop()

# ==========================================================
# Load Pricing Data
# ==========================================================

try:

    premium_quotes = loader.load_premium_quotes()

    premium_summary = loader.load_premium_summary()

    pricing_report = loader.load_pricing_report()

    premium_leakage = loader.load_premium_leakage()

except Exception as e:

    st.error(f"Unable to load pricing analytics.\n\n{e}")

    st.stop()

# ==========================================================
# Helper Functions
# ==========================================================


def format_currency(value):

    try:

        value = float(value)

        if abs(value) >= 1_000_000:

            return f"₹{value/1_000_000:.2f}M"

        if abs(value) >= 1_000:

            return f"₹{value:,.0f}"

        return f"₹{value:.2f}"

    except Exception:

        return value


def metric_value(key, default=None):

    if isinstance(premium_summary, dict):

        return premium_summary.get(key, default)

    return default


# ==========================================================
# Header
# ==========================================================

st.title("💰 Pricing Analytics")

st.caption(
    "Premium recommendations, pricing performance and portfolio profitability."
)

st.divider()

# ==========================================================
# Executive KPI Cards
# ==========================================================

st.subheader("Executive Pricing Summary")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:

    st.metric(
        "Portfolio Premium",
        format_currency(metric_value("total_portfolio_premium")),
    )

with kpi2:

    st.metric(
        "Expected Claims",
        format_currency(metric_value("total_expected_claims")),
    )

with kpi3:

    st.metric(
        "Average Premium",
        format_currency(metric_value("average_premium")),
    )

with kpi4:

    st.metric(
        "Portfolio Profit",
        format_currency(metric_value("total_profit_margin")),
    )

kpi5, kpi6, kpi7, kpi8 = st.columns(4)

with kpi5:

    st.metric(
        "Insured Lives Priced",
        f"{metric_value('rows',0):,}",
    )

with kpi6:

    st.metric(
        "Avg Claim Cost",
        format_currency(metric_value("average_claim_cost")),
    )

with kpi7:

    st.metric(
        "Loading Factor",
        metric_value("average_loading_factor"),
    )

with kpi8:

    st.metric(
        "Maximum Premium",
        format_currency(metric_value("maximum_premium")),
    )

st.divider()

# ==========================================================
# Portfolio Mix
# ==========================================================

st.subheader("Portfolio Composition")

left, right = st.columns(2)

# ----------------------------------------------------------
# Risk Distribution
# ----------------------------------------------------------

with left:

    risk_distribution = None

    if isinstance(premium_summary, dict):

        risk_distribution = premium_summary.get("risk_distribution")

    if isinstance(risk_distribution, dict):

        risk_df = pd.DataFrame({

            "Risk Class": risk_distribution.keys(),

            "Insured Lives": risk_distribution.values(),

        })

        fig = px.pie(

            risk_df,

            names="Risk Class",

            values="Policies",

            hole=0.55,

            title="Risk Distribution",

        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:

        st.info("Risk distribution unavailable.")

# ----------------------------------------------------------
# Underwriting Distribution
# ----------------------------------------------------------

with right:

    underwriting_distribution = None

    if isinstance(premium_summary, dict):

        underwriting_distribution = premium_summary.get(
            "underwriting_distribution"
        )

    if isinstance(underwriting_distribution, dict):

        uw_df = pd.DataFrame({

            "Decision": underwriting_distribution.keys(),

            "Insured Lives": underwriting_distribution.values(),

        })

        fig = px.pie(

            uw_df,

            names="Decision",

            values="Insured Lives",

            hole=0.55,

            title="Underwriting Decisions",

        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:

        st.info("Underwriting summary unavailable.")

st.divider()

# ==========================================================
# Premium Leakage Analysis
# ==========================================================

st.subheader("Premium Leakage Analysis")

if (
    isinstance(premium_leakage, pd.DataFrame)
    and not premium_leakage.empty
):

    if len(premium_leakage.columns) >= 2:

        chart_type = st.radio(
            "Chart Type",
            ["Bar", "Line"],
            horizontal=True,
        )

        if chart_type == "Bar":

            fig = px.bar(
                premium_leakage,
                x=premium_leakage.columns[0],
                y=premium_leakage.columns[1],
                title="Premium Leakage",
            )

        else:

            fig = px.line(
                premium_leakage,
                x=premium_leakage.columns[0],
                y=premium_leakage.columns[1],
                markers=True,
                title="Premium Leakage",
            )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:

        st.dataframe(
            premium_leakage,
            use_container_width=True,
        )

else:

    st.info("Premium leakage data unavailable.")

st.divider()

# ==========================================================
# Sample Premium Quotes
# ==========================================================

st.subheader("Sample Premium Quotes")

if (
    isinstance(premium_quotes, pd.DataFrame)
    and not premium_quotes.empty
):

    display_df = premium_quotes.copy()

    preferred_columns = [
        "row_id",
        "risk_class_label",
        "predicted_claim_cost",
        "recommended_premium",
        "underwriting_flag",
    ]

    available_columns = [
        col
        for col in preferred_columns
        if col in display_df.columns
    ]

    if available_columns:

        display_df = display_df[available_columns]

    st.dataframe(
        display_df.head(25),
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info("Premium quotes unavailable.")

st.divider()

# ==========================================================
# Pricing Model Performance
# ==========================================================

st.subheader("Model Performance")

if (
    isinstance(pricing_report, dict)
    and "training" in pricing_report
):

    training = pricing_report["training"]

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "MAE",
            f"{training.get('mae',0):.2f}",
        )

    with c2:

        st.metric(
            "RMSE",
            f"{training.get('rmse',0):.2f}",
        )

    with c3:

        st.metric(
            "R² Score",
            f"{training.get('r2',0):.3f}",
        )

else:

    st.info("Training metrics unavailable.")

st.divider()

# ==========================================================
# Business Insights
# ==========================================================

st.subheader("Business Insights")

left, right = st.columns(2)

with left:

    if isinstance(premium_summary, dict):

        risk_dist = premium_summary.get(
            "risk_distribution",
            {},
        )

        if risk_dist:

            largest_segment = max(
                risk_dist,
                key=risk_dist.get,
            )

            st.success(
                f"""
Largest portfolio segment:

**{largest_segment}**

Policies:

**{risk_dist[largest_segment]:,}**
"""
            )

        else:

            st.info(
                "Risk distribution unavailable."
            )

with right:

    if isinstance(premium_summary, dict):

        st.info(
            f"""
Average loading factor:

**{premium_summary.get('average_loading_factor','N/A')}**

Average premium:

**{format_currency(metric_value('average_premium'))}**

Expected claims:

**{format_currency(metric_value('total_expected_claims'))}**
"""
        )

st.divider()

# ==========================================================
# Pricing Configuration
# ==========================================================

with st.expander("Pricing Model Details"):

    if isinstance(pricing_report, dict):

        metadata = pricing_report.get(
            "metadata",
            {}
        )

        premium = pricing_report.get(
            "premium",
            {}
        )

        if metadata:

            st.subheader("Model Metadata")

            st.json(metadata)

        if premium:

            st.subheader("Premium Summary")

            st.json(premium)

    else:

        st.write(pricing_report)

# ==========================================================
# Raw Data
# ==========================================================

with st.expander("View Raw Pricing Data"):

    tab1, tab2, tab3 = st.tabs(
        [
            "Premium Quotes",
            "Premium Leakage",
            "Pricing Report",
        ]
    )

    with tab1:

        st.dataframe(
            premium_quotes,
            use_container_width=True,
        )

    with tab2:

        st.dataframe(
            premium_leakage,
            use_container_width=True,
        )

    with tab3:

        if isinstance(pricing_report, dict):

            st.json(pricing_report)

        else:

            st.write(pricing_report)