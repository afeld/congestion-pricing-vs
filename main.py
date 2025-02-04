from urllib.parse import urlencode

import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache_data
def get_entrances():
    # https://data.ny.gov/Transportation/MTA-Congestion-Relief-Zone-Vehicle-Entries-Beginni/t6yz-b64h/about_data
    params = urlencode(
        {
            "$select": "date_extract_woy(toll_date) AS week, SUM(crz_entries) AS count",
            "$group": "week",
        }
    )
    return pd.read_csv(f"https://data.ny.gov/resource/t6yz-b64h.csv?{params}")


st.title("MTA Congestion Relief Zone Vehicle Entries")

entrances = get_entrances()
entrances

fig = px.line(
    entrances,
    x="week",
    y="count",
    title="Vehicle entries by week of the year",
)
st.plotly_chart(fig)
