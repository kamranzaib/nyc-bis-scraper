import geopandas as gpd

def clean_pluto(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Cleans and standardizes the PLUTO GeoDataFrame.

    - Detects BBL column regardless of case
    - Converts BBL to 10-digit string
    - Normalizes all column names to lowercase
    """
    original_columns = list(gdf.columns)
    bbl_col = next((col for col in original_columns if col.lower() == "bbl"), None)

    if not bbl_col:
        raise ValueError(f"'bbl' column not found. Columns were: {original_columns}")

    # Create new 'bbl' column from original BBL column before renaming
    gdf['bbl'] = gdf[bbl_col].astype(str).str.zfill(10)

    # Now normalize column names
    gdf.columns = [col.lower() for col in gdf.columns]

    # Drop rows with null BBL just in case
    gdf = gdf.dropna(subset=['bbl'])

    # Drop duplicate column names if they somehow appear
    gdf = gdf.loc[:, ~gdf.columns.duplicated()]

    return gdf