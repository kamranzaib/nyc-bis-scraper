from sqlalchemy import create_engine

def load_to_postgis(gdf, table_name, db_url, if_exists="replace"):
    if gdf.empty:
        print(f"⚠️ Skipping load: {table_name} is empty.")
        return
    engine = create_engine(db_url)
    gdf.to_postgis(table_name, engine, if_exists=if_exists, index=False)
    print(f"✅ Loaded {len(gdf)} records into PostGIS table '{table_name}'")