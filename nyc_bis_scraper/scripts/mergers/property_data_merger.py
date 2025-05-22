import pandas as pd
import os
from pathlib import Path
from config import db_url

def merge_property_data(
    base_path="data/final_properties.csv",
    permits_path="data/properties_with_permits.csv",
    sales_path="data/properties_with_sales.csv",
    output_path="data/properties_master.csv"
):
    """
    Merge property data with improved aggregation of permits and sales
    """
    print("=== MERGING PROPERTY DATA ===")
    
    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 1) Load base parcels with string data types for consistency
    print(f"Loading base properties from {base_path}...")
    base = pd.read_csv(base_path, dtype=str, low_memory=False)
    print(f"Loaded {len(base):,} base properties")
    
    # 2) Aggregate permits: list all job__ by BIN
    print(f"Loading and aggregating permits from {permits_path}...")
    perm = pd.read_csv(permits_path, dtype=str, low_memory=False)
    
    # Verify BIN column exists
    if "BIN" not in perm.columns:
        print("Warning: 'BIN' column not found in permits file")
        print(f"Available columns: {', '.join(perm.columns[:10])}...")
        return None
    
    # Check for job___ column
    job_columns = [col for col in perm.columns if col.startswith('job') and col.endswith('_')]
    job_column = job_columns[0] if job_columns else "job__"
    
    if job_column not in perm.columns:
        print(f"Warning: '{job_column}' column not found in permits file")
        print(f"Available columns: {', '.join(perm.columns[:10])}...")
        # Look for alternative permit columns we could use
        alt_permit_cols = [col for col in perm.columns if 'permit' in col.lower() or 'job' in col.lower()]
        if alt_permit_cols:
            job_column = alt_permit_cols[0]
            print(f"Using alternative column for permits: '{job_column}'")
        else:
            # Create empty permit aggregation if no columns found
            perm_agg = pd.DataFrame(columns=["BIN", "all_permits"])
            
    if job_column in perm.columns:
        perm_agg = (
            perm
                .dropna(subset=[job_column])                # only rows with a permit
                .groupby("BIN")[job_column]
                .agg(lambda jobs: ";".join(sorted(set(jobs))))
                .rename("all_permits")
                .reset_index()
        )
        print(f"Aggregated permits for {len(perm_agg):,} unique BINs")
    
    # 3) Aggregate sales: take the single most recent sale per BBL
    print(f"Loading and aggregating sales from {sales_path}...")
    sales = pd.read_csv(sales_path, dtype=str, low_memory=False)
    
    # Verify BBL column exists
    if "BBL" not in sales.columns:
        print("Warning: 'BBL' column not found in sales file")
        print(f"Available columns: {', '.join(sales.columns[:10])}...")
        return None
    
    # Check for sale_date and sale_price columns
    date_columns = [col for col in sales.columns if 'date' in col.lower() and 'sale' in col.lower()]
    price_columns = [col for col in sales.columns if 'price' in col.lower() and 'sale' in col.lower()]
    
    date_column = date_columns[0] if date_columns else "sale_date"
    price_column = price_columns[0] if price_columns else "sale_price"
    
    if date_column not in sales.columns:
        print(f"Warning: '{date_column}' column not found in sales file")
        print(f"Available columns: {', '.join(sales.columns[:10])}...")
        sales_agg = pd.DataFrame(columns=["BBL", date_column, price_column])
    else:
        # Parse dates with error handling
        sales[date_column] = pd.to_datetime(sales[date_column], errors="coerce")
        
        # Check if price column exists
        if price_column not in sales.columns and price_columns:
            price_column = price_columns[0]
        
        # Create the columns list dynamically based on what's available
        agg_columns = ["BBL", date_column]
        if price_column in sales.columns:
            agg_columns.append(price_column)
        
        sales_agg = (
            sales
                .dropna(subset=[date_column])
                .sort_values(date_column)
                .groupby("BBL")
                .last()[agg_columns[1:]]  # Skip the BBL column since it's the index
                .reset_index()
        )
        print(f"Aggregated sales for {len(sales_agg):,} unique BBLs")
    
    # 4) Merge back onto base parcels
    print("Merging aggregated data with base properties...")
    master = base.merge(perm_agg, on="BIN", how="left")
    master = master.merge(sales_agg, on="BBL", how="left")
    
    # 5) Write out one row per parcel
    master.to_csv(output_path, index=False)
    print(f"✅ Successfully wrote {len(master):,} rows to {output_path} (one per parcel)")
    
    return master

if __name__ == "__main__":
    merge_property_data()