from urllib.parse import urlencode

import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache_data
def get_entrances():
    """https://data.ny.gov/Transportation/MTA-Congestion-Relief-Zone-Vehicle-Entries-Beginni/t6yz-b64h/about_data"""

    params = urlencode(
        {
            "$select": "date_extract_woy(toll_date) AS week, SUM(crz_entries) AS count_included, SUM(excluded_roadway_entries) AS count_excluded",
            "$group": "week",
        }
    )
    entrances = pd.read_csv(f"https://data.ny.gov/resource/t6yz-b64h.csv?{params}")

    entrances["count"] = entrances["count_included"] + entrances["count_excluded"]

    return entrances


@st.cache_data
def get_ridership():
    """https://data.ny.gov/Transportation/MTA-Daily-Ridership-and-Traffic-Beginning-2020/sayj-mze2/about_data"""

    params = urlencode(
        {
            "$select": "date_extract_woy(date) AS week, SUM(count) AS subway_ridership",
            "$group": "week",
            "$where": "date >= '2025-01-05' AND mode = 'Subway'",
            "$order": "week",
        }
    )
    ridership = pd.read_csv(f"https://data.ny.gov/resource/sayj-mze2.csv?{params}")

    return ridership


def line_plot(df, **kwargs):
    fig = px.line(df, **kwargs)

    # have Y axis start at zero
    y_col = kwargs["y"]
    max_y = df[y_col].max()
    fig.update_yaxes(range=[0, max_y * 1.1])

    st.plotly_chart(fig)


def run():
    st.title("MTA Congestion Relief Zone Vehicle Entries")

    entrances = get_entrances()
    entrances

    line_plot(
        entrances,
        x="week",
        y="count",
        title="Vehicle entries by week of the year",
    )

    ridership = get_ridership()
    ridership

    line_plot(
        ridership,
        x="week",
        y="subway_ridership",
        title="Subway ridership by week",
    )


run()
