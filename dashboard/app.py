import os
import streamlit as st
import pandas as pd
from pyathena import connect

REGION = "eu-north-1"
S3_STAGING = "s3://airquality-lake-338534047403/athena-results/"

# On Streamlit Cloud creds come from secrets; locally from ~/.aws
try:
    if "AWS_ACCESS_KEY_ID" in st.secrets:
        os.environ["AWS_ACCESS_KEY_ID"] = st.secrets["AWS_ACCESS_KEY_ID"]
        os.environ["AWS_SECRET_ACCESS_KEY"] = st.secrets["AWS_SECRET_ACCESS_KEY"]
except Exception:
    pass

st.set_page_config(page_title="US Air Quality vs Weather", layout="wide")

@st.cache_resource
def get_conn():
    return connect(s3_staging_dir=S3_STAGING, region_name=REGION)

@st.cache_data(ttl=600)
def load_data():
    q = "SELECT * FROM airquality.mart_pm25_weather ORDER BY measured_at"
    df = pd.read_sql(q, get_conn())
    df["measured_at"] = pd.to_datetime(df["measured_at"])
    return df

st.title("US Air Quality vs Weather")
st.caption("Hourly PM2.5 across 5 US metros joined to local weather. Sources: OpenAQ (AirNow) + Open-Meteo. Pipeline: AWS Lambda, S3, Athena, dbt.")

df = load_data()

metros = sorted(df["metro"].unique())
picked = st.multiselect("Cities", metros, default=metros)
d = df[df["metro"].isin(picked)]

c1, c2, c3 = st.columns(3)
c1.metric("Readings", len(d))
c2.metric("Avg PM2.5 (ug/m3)", round(d["pm25_ugm3"].mean(), 1))
c3.metric("Hours over WHO", int(d["over_who_daily"].sum()))

st.subheader("PM2.5 over time")
pivot = d.pivot_table(index="measured_at", columns="metro", values="pm25_ugm3", aggfunc="mean")
st.line_chart(pivot)

st.subheader("Does wind clear the air?")
st.scatter_chart(d, x="wind_kmh", y="pm25_ugm3", color="metro")
