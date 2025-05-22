# scripts/test_postgis_connection.py
from sqlalchemy import create_engine, text
from config import db_url

engine = create_engine(db_url())

with engine.connect() as conn:
    result = conn.execute(text("SELECT version(), PostGIS_Full_Version();"))
    for row in result:
        print(row)
