#!/usr/bin/env python3
"""
pluto_arcgis_extractor.py

Fetches the full MapPLUTO parcel layer from the NYC ArcGIS FeatureServer
and writes it to GeoJSON (or Shapefile) in a local directory.

Usage:
    python pluto_arcgis_extractor.py \
        --top 2000 \
        --output-dir data/pluto_data/ \
        --output-file pluto.geojson

Options:
    --top           Number of records per request (default: 2000)
    --output-dir    Directory to save output files (default: data/pluto_data/)
    --output-file   Filename for the GeoJSON output (default: pluto.geojson)
"""
import os
import sys
import argparse
import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from config import db_url
# Base URL for MapPLUTO FeatureServer layer 0
BASE_URL = (
    "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/"
    "MAPPLUTO/FeatureServer/0/query"
)


def fetch_pluto(top=2000, skip=0):
    """
    Fetches MapPLUTO parcels in pages via ArcGIS REST.
    Returns a GeoDataFrame of all parcels.
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
            print(f"Error fetching data: {resp.status_code}\n{resp.text}")
            sys.exit(1)
        data = resp.json()
        features = data.get('features', [])
        if not features:
            break
        # Convert Esri JSON features to GeoDataFrame
        records = []
        for feat in features:
            attr = feat.get('attributes', {})
            geom = feat.get('geometry')
            if geom:
               geom = shape({
    'type': 'Polygon',
    'coordinates': geom['rings']
})
            else:
                geom = None
            records.append({**attr, 'geometry': geom})
        gdf_chunk = gpd.GeoDataFrame(records, crs="EPSG:4326")
        chunks.append(gdf_chunk)
        skip += top
    if chunks:
        return gpd.GeoDataFrame(pd.concat(chunks, ignore_index=True), crs=chunks[0].crs)
    return gpd.GeoDataFrame(columns=['geometry'])


def main():
    parser = argparse.ArgumentParser(
        description="Extract MapPLUTO parcels via ArcGIS REST API"
    )
    parser.add_argument(
        '--top', type=int, default=2000,
        help='Records per request (page size)'
    )
    parser.add_argument(
        '--output-dir', type=str, default='data/pluto_data/',
        help='Directory to save output files'
    )
    parser.add_argument(
        '--output-file', type=str, default='pluto.geojson',
        help='Output filename (GeoJSON)'
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    gdf = fetch_pluto(top=args.top)
    print(f"Fetched {len(gdf)} parcels with {len(gdf.columns)} fields.")

    out_path = os.path.join(args.output_dir, args.output_file)
    print(f"Writing GeoJSON to {out_path}")
    gdf.to_file(out_path, driver='GeoJSON')

    # Optionally, write Shapefile as well
    shp_dir = os.path.join(args.output_dir, 'shapefile')
    os.makedirs(shp_dir, exist_ok=True)
    print(f"Writing Shapefile to {shp_dir}")
    gdf.to_file(os.path.join(shp_dir, "pluto.shp")) 

    from sqlalchemy import create_engine
    engine = create_engine(db_url())
    gdf.to_postgis("parcels", engine, if_exists="replace", index=False)
    print("✅ Loaded parcels into PostGIS table 'parcels'")

if __name__ == '__main__':
    main()
