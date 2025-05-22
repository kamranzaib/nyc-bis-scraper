from config import db_url
from etl.extract.fetch_footprints import fetch_footprints
from etl.transform import bin_bb_mapper
from etl.load.load_to_postgis import load_to_postgis
import pandas as pd

def main():
    print("🚀 Starting footprints pipeline...")

    gdf = fetch_footprints()
    bin_bbl_df = bin_bb_mapper.extract_bin_bbl(gdf)

    bin_bbl_df.to_csv("data/api_data/bin_to_bbl_mapping.csv", index=False)
    print("✅ Saved bin_to_bbl_mapping.csv")

    load_to_postgis(gdf, "footprints", db_url())

if __name__ == "__main__":
    main()