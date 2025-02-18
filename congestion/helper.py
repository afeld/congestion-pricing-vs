from urllib.parse import urlencode

import pandas as pd


def ny_data_request(
    dataset_id: str,
    host="data.ny.gov",
    params: dict = None,
):
    """https://dev.socrata.com/consumers/getting-started.html"""

    params_str = urlencode(params or {})
    return pd.read_csv(f"https://{host}/resource/{dataset_id}.csv?{params_str}")
