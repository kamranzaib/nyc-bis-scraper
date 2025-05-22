from etl.extract.fetch_pluto import fetch_pluto
from etl.transform.clean_pluto import clean_pluto
from etl.load.load_to_postgis import load_to_postgis
from config import db_url  # assumes your db_url() function lives here

def main():
    print("🚀 Starting PLUTO parcel ETL pipeline...")

    # Extract
    gdf = fetch_pluto()
    print(f"📥 Extracted {len(gdf)} raw records")

    # Transform
    cleaned = clean_pluto(gdf)
    print(f"🧼 Cleaned down to {len(cleaned)} valid records")

    # Load
    load_to_postgis(cleaned, table_name="parcels", db_url=db_url())

if __name__ == "__main__":
    main()