# scripts/extractors/sales.py

from sodapy import Socrata
import pandas as pd
import datetime
from config import db_url
def fetch_sales(last_n_days: int = 5*365,
                resource_id: str = "usep-8jbt") -> pd.DataFrame:
    """
    Pull DOF Residential Sales for the last N days,
    detect whether the API returns 'bbl' or rebuild from 'borough'/'block'/'lot',
    and expose manual‑friendly sales columns.
    """
    client = Socrata("data.cityofnewyork.us", None)
    cutoff = (datetime.datetime.now() - datetime.timedelta(days=last_n_days))\
             .strftime("%Y-%m-%dT00:00:00")
    where  = f"sale_date >= '{cutoff}'"
    records = client.get(resource_id, where=where, limit=500_000)
    df = pd.DataFrame.from_records(records)
    print("Sales API columns:", df.columns.tolist())

    # 1) If there's already a 'bbl' field, use it:
    if 'bbl' in df.columns:
        df['BBL'] = df['bbl'].astype(str)

    # 2) Otherwise, rebuild from 'borough','block','lot':
    elif all(col in df.columns for col in ('borough','block','lot')):
        # map text borough to its digit code
        borough_map = {
            'MANHATTAN': '1',
            'BRONX':     '2',
            'BROOKLYN':  '3',
            'QUEENS':    '4',
            'STATEN ISLAND': '5'
        }
        # uppercase and map
        df['boro_code'] = df['borough'].str.upper().map(borough_map)
        df['block_padded'] = df['block'].astype(int).astype(str).str.zfill(5)
        df['lot_padded']   = df['lot'].astype(int).astype(str).str.zfill(4)
        df['BBL'] = df['boro_code'] + df['block_padded'] + df['lot_padded']
        df.drop(columns=['boro_code','block_padded','lot_padded'], inplace=True)

    else:
        raise KeyError(
            "Sales dataset missing both 'bbl' and ['borough','block','lot']; "
            f"got: {df.columns.tolist()}"
        )

    # 3) Expose your manual‑style sales columns:
    df['SALE DATE']                   = df.get('sale_date')
    df['SALE PRICE']                  = df.get('sale_price')
    df['NEIGHBORHOOD']                = df.get('neighborhood')
    df['BUILDING CLASS AT TIME OF SALE'] = df.get('building_class_at_time_of_sale')

    return df

def main(config=None):
    df = fetch_sales()
    df.to_csv("data/sales.csv", index=False)
    print("✅ Saved data/sales.csv")
