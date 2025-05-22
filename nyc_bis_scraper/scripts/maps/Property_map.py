# scripts/maps/property_info_map.py

import pandas as pd
import geopandas as gpd
import folium
import ast
from shapely.geometry import shape, mapping
import random
from config import db_url

# 1) Load your fully merged master file
df = pd.read_csv("/Users/kamranxeb/Desktop/nyc-bis-scraper/data/properties_master.csv", low_memory=False)

# Print available columns to help debug
print("Available columns in the dataset:")
print(df.columns.tolist())

# 2) Drop rows without geometry
df = df.dropna(subset=["geometry_x"])
print(f"DataFrame shape after dropping NA geometry: {df.shape}")

# 3) Parse the geometry_x JSON-string to actual shapely geometries
def parse_geom(geo_str):
    try:
        geo_dict = ast.literal_eval(geo_str)
        return shape(geo_dict)
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing geometry: {e}")
        print(f"Problematic geometry string: {geo_str[:100]}...")
        return None

# Apply the function and drop rows where geometry parsing failed
df["geometry"] = df["geometry_x"].apply(parse_geom)
df = df.dropna(subset=["geometry"])
print(f"DataFrame shape after parsing geometry: {df.shape}")

# 4) Create a GeoDataFrame and ensure it's in EPSG:4326
gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

# 5) Sample the data to a manageable size - only take 1000 rows for testing
# Comment out this line if you want to use the full dataset
gdf = gdf.sample(n=1000, random_state=42)
print(f"Sampled DataFrame shape: {gdf.shape}")

# Print a sample row to see what data is available
print("\nSample row data (first row):")
sample_row = gdf.iloc[0]
for col in gdf.columns:
    if col != "geometry" and col != "geometry_x" and col != "geometry_y":
        print(f"{col}: {sample_row.get(col, 'N/A')}")

# 6) Build FeatureCollection with improved visibility
features = []
for idx, row in gdf.iterrows():
    # Print progress for every 100 rows
    if idx % 100 == 0:
        print(f"Processing row {idx}/{len(gdf)}")
    
    try:
        # Create properties dict
        props = {}
        
        # Add all available columns as properties (except geometry columns)
        for col in gdf.columns:
            if col not in ["geometry", "geometry_x", "geometry_y"]:
                if pd.notna(row[col]):
                    # Handle different data types appropriately
                    if isinstance(row[col], (int, float)) and col in ["YearBuilt", "YearAlter2", "UnitsRes", "UnitsTotal", "BldgArea"]:
                        props[col] = int(row[col]) if col != "BldgArea" else f"{int(row[col]):,}"
                    else:
                        props[col] = str(row[col])
                else:
                    props[col] = "N/A"
        
        # Add a random color for better visibility
        props["color"] = random.choice(["#FF5555", "#5555FF", "#55FF55", "#FFAA55", "#FF55FF", "#55FFFF"])
        
        # Create and add the feature
        features.append({
            "type": "Feature",
            "geometry": mapping(row.geometry),
            "properties": props
        })
    except Exception as e:
        print(f"Error processing row {idx}: {e}")
        continue

print(f"Total features generated: {len(features)}")

# Debug - print first feature if available
if features:
    print("Sample feature properties:", list(features[0]["properties"].keys())[:10], "...")
else:
    print("⚠️  No features generated at all!")
    import sys; sys.exit(1)

geojson = {"type": "FeatureCollection", "features": features}

# 7) Render map with improved visibility
m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

def style_fn(feature):
    # Use the random color assigned to each property
    color = feature["properties"].get("color", "#CCCCCC")
    return {
        "fillColor": color,
        "color": "#000000",  # Black outline
        "weight": 2,         # Thicker outline
        "fillOpacity": 0.7   # More opaque fill
    }

# Determine which fields to show in tooltip based on what's available
# Start with these commonly useful fields if available
tooltip_fields = []
tooltip_aliases = []

field_mapping = {
    "BIN": "BIN:",
    "Address": "Address:",
    "OwnerName": "Owner:",
    "YearBuilt": "Built:",
    "YearAlter2": "Renovated:",
    "BldgClass": "Building Class:",
    "LandUse": "Land Use:",
    "BldgArea": "Building Area:",
    "UnitsRes": "Residential Units:",
    "UnitsTotal": "Total Units:",
    "Block": "Block:",
    "Lot": "Lot:",
    "BBL": "BBL:",
    "Borough": "Borough:"
}

# Add fields that actually exist in the data
for field, alias in field_mapping.items():
    if field in gdf.columns:
        tooltip_fields.append(field)
        tooltip_aliases.append(alias)

# Create tooltip with available fields
tooltip = folium.GeoJsonTooltip(
    fields=tooltip_fields,
    aliases=tooltip_aliases,
    localize=True,
    labels=True,
    sticky=True  # Make tooltip stay open when clicked
)

# Add features to map
folium.GeoJson(
    geojson,
    style_function=style_fn,
    tooltip=tooltip,
    highlight_function=lambda x: {"weight": 4, "fillOpacity": 0.9}  # Highlight on hover
).add_to(m)

# Add a layer control to toggle the property layer
folium.LayerControl().add_to(m)

# Save the map
m.save("nyc_property_map_enhanced.html")
print("Map saved to nyc_property_map_enhanced.html")