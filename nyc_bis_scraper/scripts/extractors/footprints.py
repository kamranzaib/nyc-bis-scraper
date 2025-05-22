#!/usr/bin/env python3
"""
csv_scraper.py

Fetches building footprints via the NYC Building Footprints OData v4 endpoint
and generates clean BIN→BBL mapping matching your old manual shapefile process.
"""
import pandas as pd
import requests
import sys
import os
import geopandas as gpd
from shapely.geometry import shape

# OData v4 endpoint for Building Footprints
API_ENDPOINT = "https://data.cityofnewyork.us/api/odata/v4/5zhs-2jue"


def fetch_from_odata(top=50000, skip=0):
    """
    Fetch Building Footprints data from the OData v4 endpoint in paged chunks.
    Returns a GeoDataFrame of the combined results with geometry parsed.
    """
    chunks = []
    while True:
        params = {"$top": top, "$skip": skip}
        print(f"Fetching OData records: skip={skip}, top={top}")
        resp = requests.get(API_ENDPOINT, params=params)
        if resp.status_code != 200:
            print(f"Error fetching data: {resp.status_code} - {resp.text}")
            sys.exit(1)
        data = resp.json().get('value', [])
        if not data:
            break
        df_chunk = pd.DataFrame(data)
        chunks.append(df_chunk)
        skip += top

    if not chunks:
        return gpd.GeoDataFrame()

    df = pd.concat(chunks, ignore_index=True)
    if 'the_geom' not in df.columns:
        print("ERROR: 'the_geom' column missing from OData response.")
        sys.exit(1)

    # Convert GeoJSON-style geometry dicts into shapely objects
    df['geometry'] = df['the_geom'].apply(shape)
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs='EPSG:4326')
    return gdf


def generate_bin_bbl_mapping(df, output_dir):
    """
    Detects BIN and BBL columns, cleans numeric formats,
    splits multi-valued BBLs, filters valid IDs, and writes
    a single BIN→BBL CSV mapping.
    """
    bin_cols = [c for c in df.columns if c.lower() == 'bin']
    bbl_cols = [c for c in df.columns if c.lower() in ('bbl', 'base_bbl')]

    if not bin_cols or not bbl_cols:
        print("ERROR: Could not find BIN and/or BBL columns.")
        print("Available columns:\n  " + "\n  ".join(df.columns))
        sys.exit(1)

    bin_col = bin_cols[0]
    bbl_col = bbl_cols[0]
    print(f"Using BIN col: {bin_col}, BBL col: {bbl_col}")

    mapping = df[[bin_col, bbl_col]].dropna()
    # Remove any trailing .0 and whitespace
    mapping[bin_col] = mapping[bin_col].astype(str).str.replace(r"\.0+$", "", regex=True).str.strip()
    mapping[bbl_col] = mapping[bbl_col].astype(str).str.replace(r"\.0+$", "", regex=True)

    # Split & explode multi-valued BBL fields
    mapping[bbl_col] = mapping[bbl_col].str.split(',')
    mapping = mapping.explode(bbl_col)
    mapping[bbl_col] = mapping[bbl_col].str.strip()

    # Filter for proper lengths
    mapping = mapping[mapping[bin_col].str.len() == 7]
    mapping = mapping[mapping[bbl_col].str.len() == 10]

    mapping = mapping.rename(columns={bin_col: 'BIN', bbl_col: 'BBL'})

    out_csv = os.path.join(output_dir, 'bin_to_bbl_mapping.csv')
    mapping.to_csv(out_csv, index=False)
    print(f"Extracted {len(mapping)} BIN→BBL mappings to {out_csv}")
