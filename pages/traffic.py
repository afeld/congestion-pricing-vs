from urllib.parse import urlencode

import pandas as pd
import streamlit as st

START = "2025-01-05"

st.markdown(
    """
# Traffic

[Source data](https://data.cityofnewyork.us/Transportation/DOT-Traffic-Speeds-NBE/i4gi-tjb9/about_data)
"""
)


@st.cache_data
def get_links():
    params = urlencode(
        {
            "$select": "DISTINCT link_id, link_name",
            "$where": f"data_as_of >= '{START}' AND borough = 'Manhattan'",
        }
    )
    links = pd.read_csv(
        f"https://data.cityofnewyork.us/resource/i4gi-tjb9.csv?{params}"
    )
    links


get_links()
