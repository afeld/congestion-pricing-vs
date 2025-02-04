from urllib.parse import urlencode

import pandas as pd
import plotly.express as px
import streamlit as st

params = urlencode(
    {
        "$select": "date_extract_woy(toll_date) AS week, SUM(crz_entries) AS count",
        "$group": "week",
    }
)
# https://data.ny.gov/Transportation/MTA-Congestion-Relief-Zone-Vehicle-Entries-Beginni/t6yz-b64h/about_data
entrances = pd.read_csv(f"https://data.ny.gov/resource/t6yz-b64h.csv?{params}")
st.dataframe(entrances)

fig = px.line(
    entrances,
    x="week",
    y="count",
    title="Vehicle entries by week of the year",
)
fig.show()
