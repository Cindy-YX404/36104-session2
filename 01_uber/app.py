"""Adapted from Streamlit's official Create an app tutorial."""
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Uber pickups in NYC", layout="wide")
st.title("Uber pickups in NYC")
st.caption("September 2014 · first 10,000 rows of the tutorial dataset")

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(Path(__file__).parent / "data/uber-raw-data-sep14.csv.gz", nrows=nrows)
    data.rename(columns=str.lower, inplace=True)
    data["date/time"] = pd.to_datetime(data["date/time"], format="%m/%d/%Y %H:%M:%S")
    assert data[["lat", "lon", "date/time"]].notna().all().all()
    return data

data_load_state = st.text("Loading data...")
data = load_data(10000)
data_load_state.text("Loading data...done (using cache)")
if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.dataframe(data)
st.subheader("Number of pickups by hour")
hist = np.histogram(data["date/time"].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(pd.DataFrame({"Pickups": hist}, index=pd.Index(range(24), name="Hour")))
hour = st.slider("Hour of day", 0, 23, 17)
filtered = data[data["date/time"].dt.hour == hour]
st.subheader(f"Map of all pickups at {hour}:00")
st.caption(f"{len(filtered):,} pickups in the selected hour; coordinates are pickup locations.")
st.map(filtered[["lat", "lon"]])
st.caption("Source: Streamlit demo Uber NYC pickup data (September 2014). The first 10,000 records are a tutorial subset, not an estimate for the full month.")
st.markdown("[Tutorial](https://docs.streamlit.io/get-started/tutorials/create-an-app) · [Original dataset](https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz)")
