import pandas as pd
import sys
from pathlib import Path
import os
from config import db_url

# Ensure project root is on PYTHONPATH to import extractor modules directly
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

# Import extractor functions
from nyc_bis_scraper.scripts.extractors.footprints import fetch_footprints
from nyc_bis_scraper.scripts.extractors.pluto import fetch_pluto
from nyc_bis_scraper.scripts.extractors.permits import fetch_permits
from nyc_bis_scraper.scripts.extractors.sales import fetch_sales

def build_master(
    output_dir: str = "data/processed",
    use_csv_backups: bool = False
):
    # 1️⃣ Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # 2️⃣ Fetch building footprints
    print("== STEP 1: FETCHING FOOTPRINTS ==")
    fp = fetch_footprints()
    print(f"Fetched {len(fp)} footprints")

    # 3️⃣ Fetch full PLUTO attributes
    print("\n== STEP 2: FETCHING PLUTO ATTRIBUTES ==")
    pl = fetch_pluto()
    print(f"Fetched {len(pl)} PLUTO records with {len(pl.columns)} columns")

    # 4️⃣ Merge footprints + PLUTO on BBL
    print("\n== STEP 3: MERGING FOOTPRINTS & PLUTO ==")
    master = fp.merge(pl, on="BBL", how="left")
    print(f"Master now has {len(master.columns)} columns after PLUTO merge")

    # 5️⃣ Fetch permits (live or from CSV backup)
    print("\n== STEP 4: FETCHING PERMITS ==")
    if use_csv_backups:
        permits = pd.read_csv(os.path.join(output_dir, "properties_with_permits.csv"), dtype={"BIN":str})
    else:
        permits = fetch_permits()
    print(f"Fetched {len(permits)} permit records")

    # 6️⃣ Drop overlapping columns (except BIN) and merge on BIN
    overlapping = [c for c in permits.columns if c in master.columns and c != "BIN"]
    if overlapping:
        print(f"Dropping {len(overlapping)} overlapping columns before permit merge: {overlapping}")
    master = master.merge(
        permits.drop(columns=overlapping),
        on="BIN",
        how="left"
    )
    print(f"Master now has {len(master.columns)} columns after permits merge")

    # 7️⃣ Fetch sales (live or from CSV backup)
    print("\n== STEP 5: FETCHING SALES ==")
    if use_csv_backups:
        sales = pd.read_csv(os.path.join(output_dir, "properties_with_sales.csv"), dtype={"BBL":str})
    else:
        sales = fetch_sales()
    print(f"Fetched {len(sales)} sales records")

    # 8️⃣ Drop overlapping columns (except BBL) and merge on BBL
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

    # 9️⃣ Write out final master CSV
    out_path = os.path.join(output_dir, "properties_master.csv")
    master.to_csv(out_path, index=False)
    print(f"✅ Saved full master to {out_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build master property dataset")
    parser.add_argument("--test", action="store_true", help="Run in test mode with limited data")
    parser.add_argument("--output-dir", default="data/processed", help="Output directory for processed data")
    parser.add_argument("--use-backups", action="store_true", help="Use CSV backups instead of live data")
    args = parser.parse_args()
    
    if args.test:
        print("Running in TEST mode with limited data")
        # Override the fetch functions to return limited data
        import nyc_bis_scraper.scripts.extractors.footprints
        import nyc_bis_scraper.scripts.extractors.pluto
        import nyc_bis_scraper.scripts.extractors.permits
        import nyc_bis_scraper.scripts.extractors.sales
        
        # Store original functions
        orig_footprints = scripts.extractors.footprints.fetch_footprints
        orig_pluto = scripts.extractors.pluto.fetch_pluto
        orig_permits = scripts.extractors.permits.fetch_permits
        orig_sales = scripts.extractors.sales.fetch_sales
        
        # Override with test versions returning limited data
        def test_fetch_footprints(*args, **kwargs):
            print("Using test version of fetch_footprints")
            return orig_footprints(max_records=20, debug=True, page_size=10)
        
        def test_fetch_pluto(*args, **kwargs):
            print("Using test version of fetch_pluto")
            # Create a small test dataframe if the original function is slow
            import pandas as pd
            df = pd.DataFrame({
                'BBL': ['1000010001', '1000010002', '1000010003'],
                'Address': ['123 Test St', '456 Demo Ave', '789 Sample Rd'],
                'ZipCode': ['10001', '10002', '10003']
            })
            return df
        
        def test_fetch_permits(*args, **kwargs):
            print("Using test version of fetch_permits")
            # Create a small test dataframe if the original function is slow
            import pandas as pd
            df = pd.DataFrame({
                'BIN': ['1000001', '1000002', '1000003'],
                'PermitType': ['NB', 'ALT1', 'DM'],
                'PermitDate': ['2023-01-01', '2023-02-01', '2023-03-01']
            })
            return df
        
        def test_fetch_sales(*args, **kwargs):
            print("Using test version of fetch_sales")
            # Create a small test dataframe if the original function is slow
            import pandas as pd
            df = pd.DataFrame({
                'BBL': ['1000010001', '1000010002', '1000010003'],
                'SalePrice': [1000000, 2000000, 3000000],
                'SaleDate': ['2023-01-01', '2023-02-01', '2023-03-01']
            })
            return df
        
        # Replace functions
        scripts.extractors.footprints.fetch_footprints = test_fetch_footprints
        scripts.extractors.pluto.fetch_pluto = test_fetch_pluto
        scripts.extractors.permits.fetch_permits = test_fetch_permits
        scripts.extractors.sales.fetch_sales = test_fetch_sales
    
    build_master(output_dir=args.output_dir, use_csv_backups=args.use_backups)
