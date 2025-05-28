import requests
import pandas as pd
from datetime import datetime, timedelta

# Socrata API endpoint for DOB Permit Issuance
BASE_URL = "https://data.cityofnewyork.us/resource/ipu4-2q9a.json"

def fetch_permits(limit=50000, where_clause=None):
    """
    Fetch DOB permits from the NYC Open Data API.
    By default, fetches permits from the last 2 years or any Emergency Work (EW) permits.
    """
    two_years_ago = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%dT%H:%M:%S.%f")
    default_where = f"(issuance_date >= '{two_years_ago}' OR permit_type = 'EW')"

    where = where_clause if where_clause else default_where
    offset = 0
    permits = []

    while True:
        params = {
            "$limit": limit,
            "$offset": offset,
            "$where": where
        }

        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        batch = response.json()

        if not batch:
            break

        permits.extend(batch)
        offset += limit

    df = pd.DataFrame(permits)
    return df

if __name__ == "__main__":
    df = fetch_permits()
    print(f"Fetched {len(df)} records")
    df.to_csv("dob_permits_raw.csv", index=False)