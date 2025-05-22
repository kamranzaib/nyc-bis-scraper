"""
Simplified test version of build_master.py
"""
import pandas as pd
import os
from pathlib import Path

# Add project root to PYTHONPATH
project_root = str(Path(__file__).parent)
import sys
sys.path.insert(0, project_root)

# Mock data for testing
footprints_df = pd.DataFrame({
    'BIN': ['1000001', '1000002', '1000003'],
    'BBL': ['1000010001', '1000010002', '1000010003'],
    'geometry': ['geom1', 'geom2', 'geom3']
})

pluto_df = pd.DataFrame({
    'BBL': ['1000010001', '1000010002', '1000010004'],
    'Address': ['123 Test St', '456 Demo Ave', '999 Other Rd'],
    'ZipCode': ['10001', '10002', '10003']
})

permits_df = pd.DataFrame({
    'BIN': ['1000001', '1000004', '1000003'],
    'PermitType': ['NB', 'ALT1', 'DM'],
    'PermitDate': ['2023-01-01', '2023-02-01', '2023-03-01']
})

sales_df = pd.DataFrame({
    'BBL': ['1000010001', '1000010005', '1000010003'],
    'SalePrice': [1000000, 2000000, 3000000],
    'SaleDate': ['2023-01-01', '2023-02-01', '2023-03-01']
})

def build_master_simple(output_dir="outputs"):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Get footprints data
    print("== STEP 1: GETTING FOOTPRINTS ==")
    fp = footprints_df
    print(f"Fetched {len(fp)} footprints")
    
    # 2. Get PLUTO data
    print("\n== STEP 2: GETTING PLUTO ATTRIBUTES ==")
    pl = pluto_df
    print(f"Fetched {len(pl)} PLUTO records with {len(pl.columns)} columns")
    
    # 3. Merge footprints + PLUTO on BBL
    print("\n== STEP 3: MERGING FOOTPRINTS & PLUTO ==")
    master = fp.merge(pl, on="BBL", how="left")
    print(f"Master now has {len(master.columns)} columns after PLUTO merge")
    
    # 4. Get permits data
    print("\n== STEP 4: GETTING PERMITS ==")
    permits = permits_df
    print(f"Fetched {len(permits)} permit records")
    
    # 5. Drop overlapping columns (except BIN) and merge on BIN
    overlapping = [c for c in permits.columns if c in master.columns and c != "BIN"]
    if overlapping:
        print(f"Dropping {len(overlapping)} overlapping columns before permit merge: {overlapping}")
    master = master.merge(
        permits.drop(columns=overlapping),
        on="BIN",
        how="left"
    )
    print(f"Master now has {len(master.columns)} columns after permits merge")
    
    # 6. Get sales data
    print("\n== STEP 5: GETTING SALES ==")
    sales = sales_df
    print(f"Fetched {len(sales)} sales records")
    
    # 7. Drop overlapping columns (except BBL) and merge on BBL
    overlapping = [c for c in sales.columns if c in master.columns and c != "BBL"]
    if overlapping:
        print(f"Dropping {len(overlapping)} overlapping columns before sales merge: {overlapping}")
    master = master.merge(
        sales.drop(columns=overlapping),
        on="BBL",
        how="left",
        suffixes=("", "_sale")
    )
    print(f"Master now has {len(master.columns)} columns after sales merge")
    
    # 8. Write out final master CSV
    out_path = os.path.join(output_dir, "properties_master_test.csv")
    master.to_csv(out_path, index=False)
    print(f"\n✅ Saved test master to {out_path}")
    
    # 9. Show the data
    print("\nFinal merged dataset:")
    print(master)
    
if __name__ == "__main__":
    build_master_simple()