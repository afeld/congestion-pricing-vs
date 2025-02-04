from urllib.parse import urlencode

import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache_data
def get_entrances():
    # https://data.ny.gov/Transportation/MTA-Congestion-Relief-Zone-Vehicle-Entries-Beginni/t6yz-b64h/about_data
    params = urlencode(
        {
            "$select": "date_extract_woy(toll_date) AS week, SUM(crz_entries) AS count_included, SUM(excluded_roadway_entries) AS count_excluded",
            "$group": "week",
        }
    )
    entrances = pd.read_csv(f"https://data.ny.gov/resource/t6yz-b64h.csv?{params}")

    entrances["count"] = entrances["count_included"] + entrances["count_excluded"]

    return entrances


def run():
    st.title("MTA Congestion Relief Zone Vehicle Entries")

    entrances = get_entrances()
    entrances

    fig = px.line(
        entrances,
        x="week",
        y="count",
        title="Vehicle entries by week of the year",
    )

    # have Y axis start at zero
    fig.update_yaxes(range=[0, entrances["count"].max() * 1.1])

    st.plotly_chart(fig)


run()
