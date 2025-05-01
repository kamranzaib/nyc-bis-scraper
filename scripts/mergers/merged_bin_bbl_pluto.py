import pandas as pd

# Load your enriched file
df = pd.read_csv('/Users/kamranxeb/Desktop/nyc-bis-scraper/building_data_enriched.csv')

# Select and rename columns
final_df = df[[
    'BIN', 'BBL', 'Borough_x', 'Block_x', 'Lot_x', 'Address_x', 'ZoneDist1_x', 'LandUse_x', 
    'OwnerName_x', 'YearBuilt_x', 'geometry_x', 'LotArea', 'BldgArea', 
    'UnitsRes', 'UnitsTotal', 'ZipCode', 'Latitude', 'Longitude'
]].rename(columns={
    'Borough_x': 'Borough',
    'Block_x': 'Block',
    'Lot_x': 'Lot',
    'Address_x': 'Address',
    'ZoneDist1_x': 'ZoneDist1',
    'LandUse_x': 'LandUse',
    'OwnerName_x': 'OwnerName',
    'YearBuilt_x': 'YearBuilt',
    'geometry_x': 'geometry'
})

# Save to final CSV
final_df.to_csv('final_properties.csv', index=False)

print("✅ Final cleaned file saved as 'final_properties.csv'")  