import streamlit as st
import boto3
import pandas as pd
from decimal import Decimal
from datetime import datetime
import plotly.express as px

# Set up
st.set_page_config(layout="wide", page_title="Energy Data Dashboard")
st.title("Renewable Energy Site Dashboard")

# DynamoDB setup
region = "us-east-1"
table_name = "energy_data"
dynamodb = boto3.resource("dynamodb", region_name=region)
table = dynamodb.Table(table_name)

# Fetch data
@st.cache_data(ttl=300)
def fetch_data():
    response = table.scan()
    data = response['Items']
    for d in data:
        for k, v in d.items():
            if isinstance(v, Decimal):
                d[k] = float(v)
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='ISO8601', errors='coerce')
    return df

df = fetch_data()

# Filters
site_ids = df['site_id'].unique()
selected_sites = st.multiselect("Filter by site", site_ids, default=list(site_ids))
filtered_df = df[df['site_id'].isin(selected_sites)]

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Energy Generated vs. Consumed")
    agg = filtered_df.groupby("site_id").agg({
        "energy_generated_kwh": "sum",
        "energy_consumed_kwh": "sum"
    }).reset_index()
    fig = px.bar(agg, x="site_id", y=["energy_generated_kwh", "energy_consumed_kwh"],
                 barmode="group", title="Total Energy Generated vs Consumed")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🚨 Anomaly Count per Site")
    anomaly_df = filtered_df[filtered_df['anomaly'] == True]
    fig2 = px.histogram(anomaly_df, x="site_id", title="Anomalies by Site")
    st.plotly_chart(fig2, use_container_width=True)

# Line Chart
st.subheader("📈 Net Energy Over Time")
fig3 = px.line(filtered_df, x="timestamp", y="net_energy_kwh", color="site_id", markers=True,
               title="Net Energy Trend")
st.plotly_chart(fig3, use_container_width=True)
