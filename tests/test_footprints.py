"""
Test script for footprints module.
"""
from scripts.extractors.footprints import fetch_footprints

print("Testing fetch_footprints with limited data...")
# Get a small dataset with debug output
df = fetch_footprints(max_records=5, debug=True, page_size=5)

print(f"\nFetched {len(df)} records")
print("Sample data:")
print(df.head())