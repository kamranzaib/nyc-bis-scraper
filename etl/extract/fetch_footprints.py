import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape

API_ENDPOINT = "https://data.cityofnewyork.us/api/odata/v4/5zhs-2jue"

def fetch_footprints(top=10000, skip=0):
    chunks = []
    while True:
        params = {"$top": top, "$skip": skip}
        print(f"Fetching records: skip={skip}")
        resp = requests.get(API_ENDPOINT, params=params)
        if resp.status_code != 200:
            raise Exception(f"Failed fetch: {resp.status_code} - {resp.text}")
        data = resp.json().get("value", [])
        if not data:
            break
        df_chunk = pd.DataFrame(data)
        chunks.append(df_chunk)
        skip += top

    df = pd.concat(chunks, ignore_index=True)
    df["geometry"] = df["the_geom"].apply(shape)
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
    return gdf