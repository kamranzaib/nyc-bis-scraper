import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape

BASE_URL = (
    "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/"
    "MAPPLUTO/FeatureServer/0/query"
)

def fetch_pluto(top=2000, skip=0):
    """
    Fetches NYC MapPLUTO parcel data via ArcGIS REST API.
    Returns a GeoDataFrame with geometry and selected fields.
    """
    chunks = []
    params = {
        'where': '1=1',
        'outFields': 'bbl,lotarea,zonedist1,zonedist2,zonedist3,zonedist4,landuse,unitsres,unitstotal',
        'f': 'json',
        'resultRecordCount': top,
    }

    while True:
        params['resultOffset'] = skip
        print(f"Fetching parcels: skip={skip}, top={top}")
        resp = requests.get(BASE_URL, params=params)
        if resp.status_code != 200:
            raise Exception(f"Failed to fetch data: {resp.status_code}\n{resp.text}")
        
        data = resp.json()
        features = data.get('features', [])
        if not features:
            break

        records = []
        for feat in features:
            attr = feat.get('attributes', {})
            geom = feat.get('geometry')
            if geom:
                geom = shape({'type': 'Polygon', 'coordinates': geom['rings']})
            records.append({**attr, 'geometry': geom})

        gdf_chunk = gpd.GeoDataFrame(records, crs="EPSG:4326")
        chunks.append(gdf_chunk)
        skip += top

    if chunks:
        return gpd.GeoDataFrame(pd.concat(chunks, ignore_index=True), crs="EPSG:4326")

    return gpd.GeoDataFrame(columns=['geometry'])