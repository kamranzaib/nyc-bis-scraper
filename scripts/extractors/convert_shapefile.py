import geopandas as gpd
import pandas as pd

def convert_shapefile():
    # Load the MapPLUTO shapefile
    print("Loading MapPLUTO shapefile...")
    pluto = gpd.read_file('/Users/kamranxeb/Downloads/nyc_mappluto_24v3_1_arc_shp/MapPLUTO.shp')
    print(f"Loaded {len(pluto)} records from shapefile")
    
    # Extract BoroCode, Block, Lot
    print("Extracting BoroCode, Block, Lot columns...")
    pluto_bbl = pluto[['BoroCode', 'Block', 'Lot']].dropna()
    
    # Build BBL as 1-digit BoroCode + 5-digit Block + 4-digit Lot
    print("Building BBL identifiers...")
    pluto_bbl['BBL'] = (
        pluto_bbl['BoroCode'].astype(int).astype(str) +
        pluto_bbl['Block'].astype(int).astype(str).str.zfill(5) +
        pluto_bbl['Lot'].astype(int).astype(str).str.zfill(4)
    )
    
    # Keep only the final BBL
    pluto_bbl = pluto_bbl[['BBL']]
    
    # Save to CSV
    output_file = 'pluto_bbls.csv'
    pluto_bbl.to_csv(output_file, index=False)
    print(f"Generated {len(pluto_bbl)} BBLs and saved to {output_file}")
    
    return pluto_bbl

if __name__ == '__main__':
    convert_shapefile()