import pandas as pd
import plotly.express as px
import streamlit as st

# https://data.ny.gov/Transportation/MTA-Congestion-Relief-Zone-Vehicle-Entries-Beginni/t6yz-b64h/about_data
entrances = pd.read_csv("https://data.ny.gov/resource/t6yz-b64h.csv")
st.dataframe(entrances)

fig = px.histogram(
    entrances,
    x="vehicle_class",
    title="Vehicle types entering the MTA Congestion Relief Zone",
)
fig.show()
