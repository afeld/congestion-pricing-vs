from urllib.parse import urlencode

import pandas as pd
import streamlit as st


def ny_data_request(
    dataset_id: str,
    host="data.ny.gov",
    params: dict = None,
):
    """https://dev.socrata.com/consumers/getting-started.html"""

    params_str = urlencode(params or {})
    return pd.read_csv(f"https://{host}/resource/{dataset_id}.csv?{params_str}")


def show_df_without_commas(df: pd.DataFrame, columns: list[str]):
    column_config = {
        column: st.column_config.NumberColumn(format="%.0f") for column in columns
    }
    st.dataframe(
        df,
        column_config=column_config,
    )
