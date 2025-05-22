#!/usr/bin/env python
"""
NYC Property Map Generator Runner

This script:
1. Merges all property data files into a master dataset
2. Creates an interactive map from the master dataset
"""

import os
import sys
from pathlib import Path
from config import db_url

from Property_map import create_property_map

# Add script directories to the path
script_dir = Path(__file__).parent.parent
sys.path.insert(0, str(script_dir / "mergers"))
sys.path.insert(0, str(script_dir / "maps"))

# Import the modules (update these import paths as needed)
from property_data_merger import merge_property_data

def main():
    print("=== NYC PROPERTY MAP GENERATOR ===")
    
    # Ensure output directories exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("outputs/html", exist_ok=True)
    
    # Step 1: Merge the property data files
    print("\n== STEP 1: MERGING PROPERTY DATA ==")
    master_file = "data/properties_master.csv"
    
    merge_property_data(
        base_path="data/final_properties.csv",
        permits_path="data/properties_with_permits.csv",
        sales_path="data/properties_with_sales.csv",
        output_path=master_file
    )
    
    # Step 2: Create the property map
    print("\n== STEP 2: GENERATING PROPERTY MAP ==")
    map_output_file = "outputs/html/nyc_property_map.html"
    
    create_property_map(
        properties_path=master_file,
        max_properties=10000,
        output_file=map_output_file
    )
    
    print(f"\n=== COMPLETE ===")
    print(f"1. Master property dataset created: {master_file}")
    print(f"2. Interactive property map saved: {map_output_file}")
    print("\nOpen the HTML file in a web browser to explore the map")
    print("You can search for properties, toggle different layers, and view detailed property information")

if __name__ == "__main__":
    main()