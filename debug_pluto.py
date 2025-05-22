import geopandas as gpd
import pandas as pd
import os
import fiona

# Check if the file exists
shapefile_path = "data/raw/pluto/MapPLUTO.shp"
print(f"Checking if file exists: {shapefile_path}")
print(f"File exists: {os.path.exists(shapefile_path)}")

# Check fiona version
print(f"Fiona version: {fiona.__version__}")

# Try to check what's in the directory
base_path = "data/raw"
if os.path.exists(base_path):
    print(f"\nContents of {base_path}:")
    for file in os.listdir(base_path):
        print(f"  - {file}")
else:
    print(f"Directory {base_path} does not exist")

# Try an alternative version of fetch_pluto with better error handling
def fetch_pluto_debug(shapefile_path: str = "data/raw/MapPLUTO.shp") -> pd.DataFrame:
    """
    Load the MapPLUTO shapefile with better error handling
    """
    try:
        if not os.path.exists(shapefile_path):
            raise FileNotFoundError(f"Shapefile not found at {shapefile_path}")
        
        # Test if fiona can read the file first
        print(f"Testing Fiona read...")
        with fiona.open(shapefile_path) as src:
            print(f"Schema: {src.schema}")
            print(f"CRS: {src.crs}")
        
        # Now try with geopandas
        print(f"Reading with GeoPandas...")
        gdf = gpd.read_file(shapefile_path)
        
        # if BBL isn't explicit, build it:
        if 'BBL' not in gdf.columns:
            gdf['BBL'] = (
                gdf['BoroCode'].astype(int).astype(str) +
                gdf['Block'].astype(int).astype(str).str.zfill(5) +
                gdf['Lot'].astype(int).astype(str).str.zfill(4)
            )
        
        # drop geometry from attributes frame
        df = pd.DataFrame(gdf.drop(columns=['geometry']))
        df['BBL'] = df['BBL'].astype(str)
        return df
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# Test the function
result = fetch_pluto_debug()
if result is not None:
    print(f"\nSuccess! Shape: {result.shape}")
    print(f"Columns: {result.columns.tolist()}")
else:
    print("\nFailed to read the file.")