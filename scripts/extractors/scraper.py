import geopandas as gpd
import pandas as pd

# Path to your shapefile
shapefile_path = "/Users/kamranxeb/Downloads/Building Footprints_20250420/geo_export_6e28fd04-f99b-4c10-b6a3-ffd4e1122f52.shp"  # Update this!

try:
    # Load the shapefile
    print("Loading shapefile...")
    gdf = gpd.read_file(shapefile_path)
    
    # Print columns
    print("\nColumns found:")
    for col in gdf.columns:
        print(f"- {col}")
    
    # Save to CSV (excluding geometry)
    df = gdf.drop(columns=['geometry'], errors='ignore')
    df.to_csv('MapPLUTO_full.csv', index=False)
    print(f"\nSaved full dataset ({len(df)} records)")
    
    # Extract BINs
    bin_columns = [col for col in df.columns if 'BIN' in col.upper()]
    if bin_columns:
        for col in bin_columns:
            bins = df[col].dropna()
            valid_bins = bins[bins.astype(str).str.len() == 7]
            valid_bins = valid_bins[~valid_bins.astype(str).str.endswith('000000')]
            
            output_path = f'nyc_bins_{col.lower()}.csv'
            pd.DataFrame(valid_bins, columns=[col]).to_csv(output_path, index=False)
            print(f"Extracted {len(valid_bins)} valid BINs to {output_path}")
    else:
        print("\nNo BIN columns found")
        print("\nFirst few rows of data:")
        print(df.head())
        
except Exception as e:
    print(f"Error: {e}")