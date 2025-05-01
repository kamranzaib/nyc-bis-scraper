import pandas as pd
import geopandas as gpd
import os

def merge_bin_bbl_with_pluto():
    # Paths
    bin_bbl_csv = 'data/bin_to_bbl_mapping.csv'
    pluto_shp = '/Users/kamranxeb/Downloads/nyc_mappluto_24v3_1_arc_shp/MapPLUTO.shp'  # Update this path!
    output_dir = 'data'
    output_csv = os.path.join(output_dir, 'bin_bbl_with_pluto_data.csv')
    
    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Load BIN → BBL mapping
    print(f"Loading BIN to BBL mapping: {bin_bbl_csv}")
    bin_bbl = pd.read_csv(bin_bbl_csv)
    print(f"  - {len(bin_bbl)} BINs loaded")
    
    # Step 2: Load MapPLUTO
    print(f"\nLoading MapPLUTO: {pluto_shp}")
    pluto = gpd.read_file(pluto_shp)
    print(f"  - {len(pluto)} PLUTO records loaded")
    
    # Step 3: Create a full BBL in PLUTO
    print("\nCreating BBL column in PLUTO...")
    # borough code is assumed already encoded inside MapPLUTO
    pluto['BORO'] = pluto['BoroCode'].astype(str)
    pluto['BLOCK'] = pluto['Block'].astype(str).str.zfill(5)
    pluto['LOT'] = pluto['Lot'].astype(str).str.zfill(4)
    pluto['BBL'] = pluto['BORO'] + pluto['BLOCK'] + pluto['LOT']
    print("\nSample PLUTO BBLs:")
    print(pluto['BBL'].head(5))
    
    # Step 4: Prepare columns for merge
    bin_bbl['BASE_BBL'] = bin_bbl['BASE_BBL'].astype(str)
    pluto['BBL'] = pluto['BBL'].astype(str)
    
    # Step 5: Merge
    print("\nMerging BIN to PLUTO based on BBL...")
    merged = bin_bbl.merge(pluto, left_on='BASE_BBL', right_on='BBL', how='left', indicator=True)
    
    # Step 6: Save merged data
    merged.to_csv(output_csv, index=False)
    print(f"\n✅ Merge complete. Merged file saved to: {output_csv}")
    
    # Step 7: Merge stats
    print("\nMerge Stats:")
    print(merged['_merge'].value_counts())
    
    # Step 8: Save a more focused dataset with just the essential columns
    essential_columns = ['BIN', 'BASE_BBL', 'Address', 'ZipCode', 'BoroCode', 'Block', 'Lot', 
                         'LandUse', 'UnitsRes', 'UnitsTotal', 'YearBuilt', 'BldgClass', 
                         'ZoneDist1', 'Landmark', 'OwnerType']
    
    # Filter only columns that exist in the merged dataframe
    available_columns = [col for col in essential_columns if col in merged.columns]
    essential_df = merged[available_columns]
    
    essential_output = os.path.join(output_dir, 'bin_bbl_essential_data.csv')
    essential_df.to_csv(essential_output, index=False)
    print(f"\nEssential data saved to: {essential_output}")

if __name__ == "__main__":
    merge_bin_bbl_with_pluto()