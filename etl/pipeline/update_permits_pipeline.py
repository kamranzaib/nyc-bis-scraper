from etl.extract.fetch_permits import fetch_permits
from etl.transform.clean_permits import clean_permits
from etl.load.load_to_postgis import load_to_postgis
from config import db_url

def main():
    print("Fetching DOB permits...")
    raw = fetch_permits()
    
    print("Cleaning permit data...")
    cleaned = clean_permits(raw)

    print("Loading to PostGIS...")
    load_to_postgis(cleaned, table_name="permits", db_url=db_url(), if_exists="replace")
    print("ETL for DOB permits completed.")

if __name__ == "__main__":
    main()