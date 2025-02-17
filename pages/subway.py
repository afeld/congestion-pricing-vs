from urllib.parse import urlencode

import pandas as pd
import plotly.express as px
import streamlit as st

START = "2025-01-05"

st.markdown(
    """
# Subway ridership

Using [MTA Subway Hourly Ridership data](https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-Beginning-2025/5wq4-mkjj/about_data), limited to the [Central Business District geofence](https://data.ny.gov/Transportation/MTA-Central-Business-District-Geofence-Beginning-J/srxy-5nxn/about_data).
"""
)


@st.cache_data
def get_fence():
    polygons = pd.read_csv("https://data.ny.gov/resource/srxy-5nxn.csv")
    return polygons["polygon"]


@st.cache_data
def get_stats():
    # https://dev.socrata.com/docs/functions/within_polygon
    polygons = get_fence()
    where_clause = " or ".join(
        f"within_polygon(georeference, '{polygon}')" for polygon in polygons
    )

    params = urlencode(
        {
            "$select": "date_trunc_ymd(transit_timestamp) AS date, SUM(ridership) AS ridership",
            "$group": "date",
            "$where": where_clause,
        }
    )
    return pd.read_csv(f"https://data.ny.gov/resource/5wq4-mkjj.csv?{params}")


def run():
    ridership = get_stats()
    ridership

    fig = px.line(
        ridership,
        x="date",
        y="ridership",
        title="Subway ridership in the Central Business District",
    )
    st.plotly_chart(fig)


run()
