from urllib.parse import urlencode

import pandas as pd
import plotly.express as px
import streamlit as st

params = urlencode(
    {
        "$select": "toll_date, SUM(crz_entries) AS count",
        "$group": "toll_date",
    }
)
# https://data.ny.gov/Transportation/MTA-Congestion-Relief-Zone-Vehicle-Entries-Beginni/t6yz-b64h/about_data
entrances = pd.read_csv(f"https://data.ny.gov/resource/t6yz-b64h.csv?{params}")
st.dataframe(entrances)

fig = px.line(
    entrances,
    x="toll_date",
    y="count",
    title="Vehicle entries by date",
)
fig.show()
