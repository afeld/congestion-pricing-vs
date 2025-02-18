from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from congestion.helper import ny_data_request

st.markdown(
    """
# Subway ridership

Using [MTA Subway Hourly Ridership data](https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-Beginning-2025/5wq4-mkjj/about_data), limited to the [Central Business District geofence](https://data.ny.gov/Transportation/MTA-Central-Business-District-Geofence-Beginning-J/srxy-5nxn/about_data).
"""
)


@st.cache_data
def get_fence():
    polygons = ny_data_request("srxy-5nxn")
    return polygons["polygon"]


def get_ridership_params(start: date, end: date):
    # https://dev.socrata.com/docs/functions/within_polygon
    polygons = get_fence()
    geo_where_clause = " or ".join(
        f"within_polygon(georeference, '{polygon}')" for polygon in polygons
    )
    where_clause = f"transit_timestamp >= '{start}' AND transit_timestamp < '{end}' AND ({geo_where_clause})"

    return {
        "$select": "date_trunc_ymd(transit_timestamp) AS date, SUM(ridership) AS ridership",
        "$group": "date",
        "$where": where_clause,
    }


@st.cache_data
def get_daily_ridership(start: date, end: date):
    """End date is not inclusive"""

    if start.year != end.year:
        raise ValueError("Start and end year must be the same")

    current_year = date.today().year
    dataset_id = "5wq4-mkjj" if start.year == current_year else "wujg-7c2s"

    params = get_ridership_params(start, end)

    ridership = ny_data_request(dataset_id, params=params)
    ridership["date"] = pd.to_datetime(ridership["date"])
    return ridership


def run():
    current_ridership = get_daily_ridership(date(2025, 1, 1), date(2025, 12, 31))
    # current_ridership

    latest_date = current_ridership["date"].max().date()
    one_year_ago = latest_date - timedelta(days=365)

    past_ridership = get_daily_ridership(date(2024, 1, 1), one_year_ago)
    # past_ridership

    assert past_ridership.shape == current_ridership.shape

    current_ridership["year"] = 2025
    past_ridership["year"] = 2024
    # make years match so they line up on the chart
    past_ridership["date"] += pd.DateOffset(years=1)

    ridership = pd.concat([current_ridership, past_ridership])

    # st.dataframe(
    #     ridership.describe(),
    #     column_config={
    #         # print the year without commas
    #         "year": st.column_config.NumberColumn(format="%.0f"),
    #     },
    # )
    # st.write(ridership.info())

    fig = px.line(
        ridership,
        x="date",
        y="ridership",
        color="year",
        # past year is dashed
        line_dash="year",
        line_dash_map={2024: "dash", 2025: "solid"},
    )

    fig.add_vline(
        x=date(2025, 1, 5),
        line_width=2,
        line_dash="solid",
        line_color="red",
        # https://github.com/plotly/plotly.py/issues/3065
        # annotation_text="Open date",
    )

    st.plotly_chart(fig)


run()
