from urllib.parse import urlencode

import pandas as pd
import streamlit as st

from congestion.helper import ny_data_request

START = "2025-01-05"

st.markdown(
    """
# Traffic

[Source data](https://data.cityofnewyork.us/Transportation/DOT-Traffic-Speeds-NBE/i4gi-tjb9/about_data)
"""
)


@st.cache_data
def get_links():
    params = {
        "$select": "DISTINCT link_id, link_name",
        "$where": f"data_as_of >= '{START}' AND borough = 'Manhattan'",
        "$order": "link_name",
    }

    links = ny_data_request("i4gi-tjb9", host="data.cityofnewyork.us", params=params)
    links


get_links()
