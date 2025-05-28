from sqlalchemy import create_engine
import geopandas as gpd
import pandas as pd

def load_to_postgis(df, table_name, db_url, if_exists="replace"):
    if df.empty:
        print(f"⚠️ Skipping load: {table_name} is empty.")
        return

    engine = create_engine(db_url)

    # Use GeoPandas for geospatial data, Pandas otherwise
    if isinstance(df, gpd.GeoDataFrame) and df.geometry.name in df.columns:
        df.to_postgis(table_name, engine, if_exists=if_exists, index=False)
    else:
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)

    print(f"✅ Loaded {len(df)} records into PostGIS table '{table_name}'")