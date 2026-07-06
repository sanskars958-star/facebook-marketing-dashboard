# ==========================================================
# FACEBOOK MARKETING ANALYTICS DASHBOARD
# ==========================================================

# -------------------------
# Import Libraries
# -------------------------

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="Facebook Marketing Dashboard",
    page_icon="",
    layout="wide"
)

# -------------------------
# Load Custom CSS
# -------------------------

def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# -------------------------
# Load Dataset
# -------------------------

df = pd.read_csv("data/Facebook_Dataset.csv")

# -------------------------
# Clean Dataset
# -------------------------

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Convert dates
df["Start Date"] = pd.to_datetime(df["Start Date"])
df["End Date"] = pd.to_datetime(df["End Date"])

# -------------------------
# Convert percentage columns to numeric
# -------------------------

df["CTR"] = (
    df["CTR"]
    .astype(str)
    .str.replace("%", "", regex=False)
    .astype(float)
)

df["ROI"] = (
    df["ROI"]
    .astype(str)
    .str.replace("%", "", regex=False)
    .astype(float)
)

# -------------------------
# Sidebar Filters
# -------------------------

st.sidebar.header("Dashboard Filters")

channel_filter = st.sidebar.multiselect(
    "Select Marketing Channel",
    options=sorted(df["Channel"].unique()),
    default=sorted(df["Channel"].unique())
)

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

age_filter = st.sidebar.multiselect(
    "Select Age Group",
    options=sorted(df["Age"].unique()),
    default=sorted(df["Age"].unique())
)

date_filter = st.sidebar.date_input(
    "Select Date Range",
    value=(
        df["Start Date"].min(),
        df["End Date"].max()
    )
)

# -------------------------
# Apply Filters
# -------------------------

filtered_df = df[
    (df["Channel"].isin(channel_filter)) &
    (df["Gender"].isin(gender_filter)) &
    (df["Age"].isin(age_filter))
]

# Date Filter
if len(date_filter) == 2:
    start_date, end_date = date_filter

    filtered_df = filtered_df[
        (filtered_df["Start Date"] >= pd.to_datetime(start_date)) &
        (filtered_df["End Date"] <= pd.to_datetime(end_date))
    ]

# -------------------------
# Dashboard Header
# -------------------------

st.markdown("""
<div class="dashboard-header">
<h1> Facebook Marketing Analytics Dashboard</h1>
<p>Campaign ROI • Revenue • Conversions • Performance Insights</p>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# KPI CARDS
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

# Revenue
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title"> Total Revenue</div>
        <div class="metric-value">
            ₹{filtered_df['Revenue'].sum():,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Marketing Spend
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title"> Marketing Spend</div>
        <div class="metric-value">
            ₹{filtered_df['Spent'].sum():,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Profit
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title"> Total Profit</div>
        <div class="metric-value">
            ₹{filtered_df['Profit'].sum():,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ROI
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title"> Average ROI</div>
        <div class="metric-value">
            {filtered_df['ROI'].mean():.2f}%
        </div>
    </div>
    """, unsafe_allow_html=True)
   
st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================================
# CHARTS - ROW 1
# ==========================================================

chart1, chart2 = st.columns(2)

# -------------------------
# Average ROI by Channel
# -------------------------

roi_channel = (
    filtered_df
    .groupby("Channel", as_index=False)["ROI"]
    .mean()
)

fig_roi = px.bar(
    roi_channel,
    x="Channel",
    y="ROI",
    color="Channel",
    text_auto=".2f"
)

fig_roi.update_layout(
    height=450,
    title_x=0.5,
    xaxis_title="Marketing Channel",
    yaxis_title="Average ROI (%)",
    showlegend=False,
    template="plotly_white"
)

with chart1:
    st.markdown("""
    <h4 style="text-align:center; margin-bottom:10px;">
        Average ROI by Channel
    </h4>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig_roi, use_container_width=True)

# -------------------------
# Revenue vs Marketing Spend
# -------------------------

revenue_spend = (
    filtered_df
    .groupby("Channel", as_index=False)[["Revenue", "Spent"]]
    .sum()
)

fig_revenue = px.bar(
    revenue_spend,
    x="Channel",
    y=["Revenue", "Spent"],
    barmode="group"
)

fig_revenue.update_layout(
    height=450,
    title_x=0.5,
    xaxis_title="Marketing Channel",
    yaxis_title="Amount",
    template="plotly_white"
)

with chart2:
    st.markdown("""
    <h4 style="text-align:center; margin-bottom:10px;">
        Revenue vs Marketing Spend
    </h4>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig_revenue, use_container_width=True)

# ==========================================================
# CHARTS - ROW 2
# ==========================================================

chart3, chart4 = st.columns(2)

# -------------------------
# Profit by Channel
# -------------------------

profit_channel = (
    filtered_df
    .groupby("Channel", as_index=False)["Profit"]
    .sum()
)

fig_profit = px.bar(
    profit_channel,
    x="Profit",
    y="Channel",
    orientation="h",
    color="Channel",
    text_auto=True
)

fig_profit.update_layout(
    height=450,
    title_x=0.5,
    xaxis_title="Profit",
    yaxis_title="Marketing Channel",
    showlegend=False,
    template="plotly_white"
)

with chart3:
    st.markdown("""
    <h4 style="text-align:center; margin-bottom:10px;">
        Profit by Marketing Channel
    </h4>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig_profit, use_container_width=True)

# -------------------------
# Revenue Trend
# -------------------------

revenue_trend = (
    filtered_df
    .groupby("Start Date", as_index=False)["Revenue"]
    .sum()
    .sort_values("Start Date")
)

fig_trend = px.line(
    revenue_trend,
    x="Start Date",
    y="Revenue",
    markers=True
)

fig_trend.update_layout(
    height=450,
    title_x=0.5,
    xaxis_title="Date",
    yaxis_title="Revenue",
    template="plotly_white"
)

with chart4:
    st.markdown("""
    <h4 style="text-align:center; margin-bottom:10px;">
        Revenue Trend
    </h4>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig_trend, use_container_width=True)

# ==========================================================
# CHARTS - ROW 3
# ==========================================================

chart5, chart6 = st.columns(2)

# -------------------------
# Approved Conversions by Channel
# -------------------------

conversion_channel = (
    filtered_df
    .groupby("Channel", as_index=False)["Approved conversion"]
    .sum()
)

fig_conversion = px.bar(
    conversion_channel,
    x="Channel",
    y="Approved conversion",
    color="Channel",
    text_auto=True
)

fig_conversion.update_layout(
    height=450,
    title_x=0.5,
    xaxis_title="Marketing Channel",
    yaxis_title="Approved Conversions",
    showlegend=False,
    template="plotly_white"
)

with chart5:
    st.markdown("""
    <h4 style="text-align:center; margin-bottom:10px;">
        Approved Conversions by Channel
    </h4>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig_conversion, use_container_width=True)

# -------------------------
# CTR Distribution
# -------------------------

fig_ctr = px.histogram(
    filtered_df,
    x="CTR",
    nbins=25
)

fig_ctr.update_layout(
    height=450,
    title_x=0.5,
    xaxis_title="CTR",
    yaxis_title="Frequency",
    template="plotly_white"
)

with chart6:
    st.markdown("""
    <h4 style="text-align:center; margin-bottom:10px;">
        CTR Distribution
    </h4>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig_ctr, use_container_width=True)

# ==========================================================
# CHARTS - ROW 4
# ==========================================================

chart7, chart8 = st.columns(2)

# -------------------------
# Spend vs Revenue Scatter Plot
# -------------------------

fig_scatter = px.scatter(
    filtered_df,
    x="Spent",
    y="Revenue",
    color="Channel",
    size="Approved conversion",
    hover_data=[
        "Campaign Id",
        "Age",
        "Gender"
    ]
)

fig_scatter.update_layout(
    height=500,
    title_x=0.5,
    xaxis_title="Marketing Spend",
    yaxis_title="Revenue",
    template="plotly_white"
)

with chart7:
    st.markdown("""
    <h4 style="text-align:center; margin-bottom:10px;">
        Marketing Spend vs Revenue
    </h4>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig_scatter, use_container_width=True)

# -------------------------
# Correlation Heatmap
# -------------------------

correlation = filtered_df[
    [
        "Impressions",
        "Clicks",
        "Spent",
        "Revenue",
        "Profit",
        "ROI",
        "CTR",
        "Approved conversion"
    ]
].corr()

fig_heatmap = px.imshow(
    correlation,
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale="Blues"
)

fig_heatmap.update_layout(
    height=500,
    title_x=0.5,
    template="plotly_white"
)

with chart8:
    st.markdown("""
    <h4 style="text-align:center; margin-bottom:10px;">
        Correlation Heatmap
    </h4>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig_heatmap, use_container_width=True)

# Convert percentage columns to numeric (example for ROI and CTR)
filtered_df["ROI"] = filtered_df["ROI"].replace('%', '', regex=True).astype(float)
filtered_df["CTR"] = filtered_df["CTR"].replace('%', '', regex=True).astype(float)

# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

st.markdown("---")
st.header("Business Insights")

best_roi = (
    filtered_df.groupby("Channel")["ROI"]
    .mean()
    .idxmax()
)

worst_roi = (
    filtered_df.groupby("Channel")["ROI"]
    .mean()
    .idxmin()
)

highest_revenue = (
    filtered_df.groupby("Channel")["Revenue"]
    .sum()
    .idxmax()
)

highest_profit = (
    filtered_df.groupby("Channel")["Profit"]
    .sum()
    .idxmax()
)

total_campaigns = filtered_df["Campaign Id"].nunique()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Performance Summary")

    st.success(f"Best ROI Channel: {best_roi}")
    st.success(f"Highest Revenue: {highest_revenue}")
    st.success(f"Highest Profit: {highest_profit}")
    st.info(f"Total Campaigns: {total_campaigns}")

with col2:
    st.subheader("Recommendations")

    st.warning(
        f"""
• Increase investment in **{best_roi}**.

• Review campaigns running on **{worst_roi}**.

• Focus on improving CTR through better creatives and audience targeting.

• Allocate more budget to high-performing channels while optimizing low-performing campaigns.
"""
    )

# ==========================================================
# CAMPAIGN PERFORMANCE DATA
# ==========================================================

st.markdown("---")
st.header("Campaign Performance Data")

search = st.text_input(
    "Search Campaign ID or Channel",
    placeholder="Type Campaign ID or Marketing Channel..."
)

table_df = filtered_df.copy()

if search:
    table_df = table_df[
        table_df["Campaign Id"].astype(str).str.contains(search, case=False)
        |
        table_df["Channel"].astype(str).str.contains(search, case=False)
    ]

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# DOWNLOAD DATA
# ==========================================================

csv = table_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Data (CSV)",
    data=csv,
    file_name="Filtered_Facebook_Campaign_Data.csv",
    mime="text/csv"
)
