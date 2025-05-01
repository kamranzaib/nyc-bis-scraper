import pandas as pd
import folium
from shapely import wkt
import geopandas as gpd
from pyproj import CRS

# Load your cleaned CSV
df = pd.read_csv('final_properties.csv')

# Drop rows with missing geometry
df = df.dropna(subset=['geometry'])

# Parse WKT into shapely objects
df['geometry'] = df['geometry'].apply(wkt.loads)

# Filter by Borough
borough_code = 'BK'
df = df[df['Borough'] == borough_code]
print(f"Properties in {borough_code}: {len(df)}")

# Sample data
df = df.sample(n=15000, random_state=42)

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry='geometry')

# Set the correct source CRS - this appears to be NY State Plane Long Island
# This is the critical step you're missing
gdf.crs = CRS('EPSG:2263')  # NY State Plane Long Island (NAD83 feet)

# Transform to WGS84
gdf = gdf.to_crs('EPSG:4326')

print("Coordinate ranges after transformation:")
print(f"X range: {gdf.geometry.bounds.minx.min()} to {gdf.geometry.bounds.maxx.max()}")
print(f"Y range: {gdf.geometry.bounds.miny.min()} to {gdf.geometry.bounds.maxy.max()}")

# Create map
m = folium.Map(location=[40.6782, -73.9442], zoom_start=12)

# Add properties to map
for idx, row in gdf.iterrows():
    folium.GeoJson(
        row.geometry.__geo_interface__,
        style_function=lambda x: {
            "fillColor": "#228B22",
            "color": "blue",
            "weight": 1,
            "fillOpacity": 0.5
        },
        tooltip=f"Address: {row.get('Address', 'N/A')}<br>Year Built: {row.get('YearBuilt', 'N/A')}"
    ).add_to(m)

# Save map
m.save(f'nyc_lots_{borough_code.lower()}_fixed.html')
print("Map saved successfully!")