import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="Facebook Marketing Dashboard",
    page_icon="",
    layout="wide"
)

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("Facebook_Dataset.csv")

    df.columns = df.columns.str.strip()

    df["Start Date"] = pd.to_datetime(
        df["Start Date"],
        dayfirst=True,
        errors="coerce"
    )

    df["End Date"] = pd.to_datetime(
        df["End Date"],
        dayfirst=True,
        errors="coerce"
    )

    numeric_cols = [
        "Impressions",
        "Clicks",
        "Spent",
        "Total Conversion",
        "Approved conversion",
        "Revenue",
        "Profit",
        "ROI",
        "CTR"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.fillna(0, inplace=True)

    df["Month"] = df["Start Date"].dt.strftime("%b")

    df["CPC"] = np.where(
        df["Clicks"] > 0,
        df["Spent"] / df["Clicks"],
        0
    )

    df["Conversion Rate"] = np.where(
        df["Clicks"] > 0,
        (df["Approved conversion"] / df["Clicks"]) * 100,
        0
    )

    return df


df = load_data()

# -----------------------------------------------------
# CSS
# -----------------------------------------------------

st.markdown("""
<style>

.main{
background:#F7F9FC;
}

h1{
color:#5B2EFF;
font-weight:700;
}

div[data-testid="stMetric"]{
background:white;
padding:15px;
border-radius:12px;
box-shadow:0px 2px 10px rgba(0,0,0,0.08);
}

</style>
""",unsafe_allow_html=True)

# -----------------------------------------------------
# TITLE
# -----------------------------------------------------

st.title("Facebook Marketing Performance Dashboard")

st.markdown(
"Interactive dashboard for analysing Facebook marketing campaigns."
)

st.divider()

# -----------------------------------------------------
# SIDEBAR
# -----------------------------------------------------

st.sidebar.header("Dashboard Filters")

channel = st.sidebar.multiselect(
    "Channel",
    sorted(df["Channel"].unique()),
    default=sorted(df["Channel"].unique())
)

gender = st.sidebar.multiselect(
    "Gender",
    sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

age = st.sidebar.multiselect(
    "Age",
    sorted(df["Age"].unique()),
    default=sorted(df["Age"].unique())
)

campaign = st.sidebar.multiselect(
    "Campaign",
    sorted(df["Campaign Id"].unique()),
    default=sorted(df["Campaign Id"].unique())
)

filtered_df = df[
    (df["Channel"].isin(channel)) &
    (df["Gender"].isin(gender)) &
    (df["Age"].isin(age)) &
    (df["Campaign Id"].isin(campaign))
]

# -----------------------------------------------------
# KPI VALUES
# -----------------------------------------------------

total_spend = filtered_df["Spent"].sum()
total_revenue = filtered_df["Revenue"].sum()
total_profit = filtered_df["Profit"].sum()

total_clicks = int(filtered_df["Clicks"].sum())
total_conversion = int(filtered_df["Approved conversion"].sum())

avg_roi = filtered_df["ROI"].mean()
avg_ctr = filtered_df["CTR"].mean()

# -----------------------------------------------------
# KPI CARDS
# -----------------------------------------------------

r1c1,r1c2,r1c3 = st.columns(3)

with r1c1:
    st.metric("Total Spend",f"${total_spend:,.0f}")

with r1c2:
    st.metric("Revenue",f"${total_revenue:,.0f}")

with r1c3:
    st.metric("Profit",f"${total_profit:,.0f}")

r2c1,r2c2,r2c3 = st.columns(3)

with r2c1:
    st.metric("Clicks",f"{total_clicks:,}")

with r2c2:
    st.metric("Approved Conversions",f"{total_conversion:,}")

with r2c3:
    st.metric("Avg ROI",f"{avg_roi:.2f}%")

st.divider()

st.subheader("Campaign Performance")
# -----------------------------------------------------
# ROW 1
# -----------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    spend_channel = (
        filtered_df
        .groupby("Channel")["Spent"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        spend_channel,
        x="Channel",
        y="Spent",
        color="Channel",
        title="Total Spend by Channel",
        text_auto=".0f"
    )

    fig.update_layout(
        height=430,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


with col2:

    revenue_channel = (
        filtered_df
        .groupby("Channel")["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        revenue_channel,
        x="Channel",
        y="Revenue",
        color="Channel",
        title="Revenue by Channel",
        text_auto=".0f"
    )

    fig.update_layout(
        height=430,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------------------------------
# ROW 2
# -----------------------------------------------------

col3, col4 = st.columns(2)

with col3:

    profit_channel = (
        filtered_df
        .groupby("Channel")["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        profit_channel,
        x="Channel",
        y="Profit",
        color="Channel",
        title="Profit by Channel",
        text_auto=".0f"
    )

    fig.update_layout(
        height=430,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


with col4:

    roi_channel = (
        filtered_df
        .groupby("Channel")["ROI"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        roi_channel,
        x="Channel",
        y="ROI",
        color="Channel",
        title="Average ROI by Channel",
        text_auto=".2f"
    )

    fig.update_layout(
        height=430,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()
# -----------------------------------------------------
# ROW 3
# -----------------------------------------------------

col5, col6 = st.columns(2)

with col5:

    clicks_channel = (
        filtered_df
        .groupby("Channel")["Clicks"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        clicks_channel,
        x="Channel",
        y="Clicks",
        color="Channel",
        title="Clicks by Channel",
        text_auto=".0f"
    )

    fig.update_layout(
        height=430,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

with col6:

    conversion_channel = (
        filtered_df
        .groupby("Channel")["Approved conversion"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        conversion_channel,
        x="Channel",
        y="Approved conversion",
        color="Channel",
        title="Approved Conversions by Channel",
        text_auto=".0f"
    )

    fig.update_layout(
        height=430,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------------------------------
# ROW 4
# -----------------------------------------------------

col7, col8 = st.columns(2)

with col7:

    gender_spend = (
        filtered_df
        .groupby("Gender")["Spent"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        gender_spend,
        names="Gender",
        values="Spent",
        title="Spend Distribution by Gender",
        hole=0.45
    )

    fig.update_layout(height=430)

    st.plotly_chart(fig, use_container_width=True)

with col8:

    age_revenue = (
        filtered_df
        .groupby("Age")["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        age_revenue,
        x="Age",
        y="Revenue",
        color="Age",
        title="Revenue by Age Group",
        text_auto=".0f"
    )

    fig.update_layout(
        height=430,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()
# -----------------------------------------------------
# MONTHLY SPEND TREND
# -----------------------------------------------------

st.subheader("Monthly Marketing Trend")

monthly = (
    filtered_df
    .groupby("Month", sort=False)[["Spent", "Revenue"]]
    .sum()
    .reset_index()
)

fig = px.line(
    monthly,
    x="Month",
    y=["Spent", "Revenue"],
    markers=True,
    title="Monthly Spend vs Revenue"
)

fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------------------------------
# SCATTER PLOT
# -----------------------------------------------------

st.subheader("Spend vs Revenue")

fig = px.scatter(
    filtered_df,
    x="Spent",
    y="Revenue",
    color="Channel",
    size="Clicks",
    hover_data=[
        "Campaign Id",
        "Age",
        "Gender"
    ],
    title="Relationship between Spend and Revenue"
)

fig.update_layout(height=550)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------------------------------
# TOP CAMPAIGNS
# -----------------------------------------------------

st.subheader("Top 10 Campaigns")

top_campaigns = (
    filtered_df
    .groupby("Campaign Id")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_campaigns,
    x="Campaign Id",
    y="Revenue",
    color="Revenue",
    text_auto=".0f",
    title="Top 10 Revenue Generating Campaigns"
)

fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------------------------------
# DATA TABLE
# -----------------------------------------------------

st.subheader("Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=450
)

# -----------------------------------------------------
# DOWNLOAD BUTTON
# -----------------------------------------------------

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset",
    data=csv,
    file_name="filtered_marketing_data.csv",
    mime="text/csv"
)

st.divider()

st.success("Dashboard Loaded Successfully ✅")