import pandas as pd
import os

def clean_pluto_data(input_file, output_file):
    # Read the full CSV
    df = pd.read_csv(input_file)

    # Step 1: Pick BBL correctly
    if 'BASE_BBL' in df.columns:
        df['BBL'] = df['BASE_BBL']
    elif 'BBL' in df.columns:
        df['BBL'] = df['BBL']
    else:
        raise ValueError("No BASE_BBL or BBL column found!")
    
    # Step 2: Columns you want to keep
    cols_to_keep = [
        'BIN', 'BBL', 'Borough', 'Block', 'Lot', 
        'Address', 'ZoneDist1', 'LandUse', 'OwnerName', 
        'YearBuilt', 'geometry'
    ]

    # Step 3: Drop missing columns safely
    available_cols = [col for col in cols_to_keep if col in df.columns]
    cleaned = df[available_cols]

    # Step 4: Optional: Remove duplicates
    cleaned = cleaned.drop_duplicates(subset=['BIN'])

    # Step 5: Save cleaned file
    cleaned.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")
    print(f"Rows after cleaning: {len(cleaned)}")

if __name__ == "__main__":
    input_csv = "data/bin_bbl_with_pluto_data.csv"   # <-- your file
    output_csv = "bin_bbl_cleaned.csv"                # <-- new cleaned file
    clean_pluto_data(input_csv, output_csv)