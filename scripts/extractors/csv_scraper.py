import pandas as pd
import os

def extract_bins_and_bbls_from_csv():
    # Path to your CSV file
    csv_path = "/Users/kamranxeb/Downloads/Building_Footprints_20250420.csv"  # Update this!
    
    try:
        # Read CSV file
        print(f"Reading CSV file: {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Print columns
        print("\nColumns found:")
        for col in df.columns:
            print(f"- {col}")
        
        # Look for columns that might contain BIN data
        bin_columns = [col for col in df.columns if 'BIN' in col.upper()]
        
        if bin_columns:
            for col in bin_columns:
                print(f"\nProcessing column: {col}")
                
                # Extract non-null values
                bins = df[col].dropna()
                
                # Convert to string and filter for valid BINs
                bins_str = bins.astype(str)
                valid_bins = bins_str[bins_str.str.len() == 7]  # BINs should be 7 digits
                valid_bins = valid_bins[~valid_bins.str.endswith('000000')]  # Remove dummy BINs
                
                # Save to CSV
                output_path = f'nyc_bins_{col.lower()}.csv'
                pd.DataFrame(valid_bins, columns=[col]).to_csv(output_path, index=False)
                print(f"Extracted {len(valid_bins)} valid BINs to {output_path}")
                
                # Display sample of valid BINs
                if len(valid_bins) > 0:
                    print(f"Sample BINs from {col}:")
                    print(valid_bins.head(10).to_string())
        else:
            print("\nNo BIN columns found by name.")
            print("Let's check columns that might contain numeric IDs...")
            
        # Look for columns that might contain BBL data
        bbl_columns = [col for col in df.columns if 'BBL' in col.upper()]
        
        if bbl_columns:
            for col in bbl_columns:
                print(f"\nFound potential BBL column: {col}")
                
                # Extract non-null values
                bbls = df[col].dropna()
                
                # Convert to string and filter for valid BBLs
                bbls_str = bbls.astype(str)
                valid_bbls = bbls_str[(bbls_str.str.len() == 10)]  # BBLs should be 10 digits
                
                # Save to CSV
                output_path = f'nyc_bbls_{col.lower()}.csv'
                pd.DataFrame(valid_bbls, columns=[col]).to_csv(output_path, index=False)
                print(f"Extracted {len(valid_bbls)} valid BBLs to {output_path}")
                
                # Display sample BBLs
                if len(valid_bbls) > 0:
                    print(f"Sample BBLs from {col}:")
                    print(valid_bbls.head(10).to_string())
        else:
            print("\nNo BBL columns found by name.")
        
            # Look for columns that might contain numeric IDs
            for col in df.columns:
                try:
                    # Check if column contains numeric values that could be BINs or BBLs
                    numeric_values = pd.to_numeric(df[col], errors='coerce').dropna()
                    
                    # Check for potential BINs (7 digits)
                    potential_bins = numeric_values[(numeric_values >= 1000000) & (numeric_values <= 5999999)]
                    
                    # Check for potential BBLs (10 digits)
                    potential_bbls = numeric_values[(numeric_values >= 1000000000) & (numeric_values <= 5999999999)]
                    
                    if len(potential_bins) > 0:
                        print(f"\nColumn '{col}' contains {len(potential_bins)} values that could be BINs")
                        print(f"Sample values: {potential_bins.head(5).tolist()}")
                        
                    if len(potential_bbls) > 0:
                        print(f"\nColumn '{col}' contains {len(potential_bbls)} values that could be BBLs")
                        print(f"Sample values: {potential_bbls.head(5).tolist()}")
                        
                except Exception as e:
                    # Skip columns that can't be converted to numeric
                    continue
        
        # Check if BBL and BIN data are in the same file
        if bin_columns and bbl_columns:
            print("\n\n=== BIN and BBL Relationship Analysis ===")
            
            # Convert to string to ensure proper matching
            df[bin_columns[0]] = df[bin_columns[0]].astype(str)
            df[bbl_columns[0]] = df[bbl_columns[0]].astype(str)
            
            # Filter for valid entries
            valid_data = df[df[bin_columns[0]].str.len() == 7]
            valid_data = valid_data[valid_data[bbl_columns[0]].str.len() == 10]
            
            print(f"Found {len(valid_data)} records with both valid BIN and BBL data")
            
            if len(valid_data) > 0:
                # Create a mapping file
                mapping_path = 'bin_to_bbl_mapping.csv'
                valid_data[[bin_columns[0], bbl_columns[0]]].to_csv(mapping_path, index=False)
                print(f"Created BIN to BBL mapping file: {mapping_path}")
                
                # Show sample
                print("Sample of BIN to BBL mapping:")
                print(valid_data[[bin_columns[0], bbl_columns[0]]].head(10).to_string())
            
        print("\nDisplaying first few rows of the dataset:")
        print(df.head().to_string())
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    extract_bins_and_bbls_from_csv()