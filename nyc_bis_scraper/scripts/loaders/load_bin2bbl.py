import pandas as pd
from sqlalchemy import create_engine, text
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from config import db_url

engine = create_engine(db_url())

# Load CSV and normalize
df = pd.read_csv("data/api_data/bin_to_bbl_mapping.csv")
df.columns = [col.strip().lower() for col in df.columns]
df = df.drop_duplicates(subset=["bin"])  # Deduplicate before loading

# Connect and create table cleanly
with engine.begin() as conn:
    print("🧹 Dropping table if it exists...")
    conn.execute(text("DROP TABLE IF EXISTS bin2bbl"))

    print("🧱 Creating table...")
    conn.execute(text("""
        CREATE TABLE bin2bbl (
            bin VARCHAR PRIMARY KEY,
            bbl VARCHAR
        )
    """))

print("📥 Inserting records...")
df.to_sql("bin2bbl", con=engine, if_exists="append", index=False)

print("✅ Loaded bin2bbl into PostGIS.")