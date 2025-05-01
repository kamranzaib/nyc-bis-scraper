from sodapy import Socrata
import pandas as pd
import datetime
import time
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

# 1) Load your BIN list
logger.info("Loading property data...")
props = pd.read_csv("final_properties.csv")
logger.info(f"First few BINs in your data: {props['BIN'].head(5).tolist()}")

# Convert BINs to strings and remove any leading/trailing whitespace
bins_list = [str(bin_val).strip() for bin_val in props["BIN"].unique()]
bins_set = set(bins_list)
logger.info(f"Found {len(bins_set)} unique BINs")

# 2) Query without date filtering first to check data
client = Socrata("data.cityofnewyork.us", None)
logger.info("Getting sample permits to inspect format...")

try:
    # Get a small sample first to inspect column names and formats
    sample_permits = client.get("ipu4-2q9a", limit=5)
    logger.info("Sample permit data:")
    for permit in sample_permits:
        logger.info(permit)
    
    # Identify the BIN column format
    bin_column = None
    for key in sample_permits[0].keys():
        if 'bin' in key.lower():
            bin_column = key
            logger.info(f"Found BIN column: {bin_column}")
            logger.info(f"Sample BIN values: {[p.get(bin_column) for p in sample_permits]}")
    
    if not bin_column:
        bin_column = "bin__"  # Default if not found
    
    # 3) Now query with date
    logger.info("Querying all permits for the last 5 years...")
    
    # Use a simpler date format and earlier cutoff
    cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=5*365)).strftime("%Y-%m-%d")
    logger.info(f"Using cutoff date: {cutoff_date}")
    
    where_clause = f"filing_date >= '{cutoff_date}'"
    logger.info(f"Query: {where_clause}")
    
    all_permits = client.get(
        "ipu4-2q9a",
        where=where_clause,
        limit=1000000
    )
    
    logger.info(f"Retrieved {len(all_permits)} total permits")
    
    # 4) Check BIN formats before filtering
    if len(all_permits) > 0:
        permit_bin_values = [p.get(bin_column) for p in all_permits[:100] if p.get(bin_column)]
        logger.info(f"Sample BIN values from permits: {permit_bin_values[:5]}")
        
        # Try converting your BINs to match format
        # Option 1: Try as-is
        filtered_permits1 = [p for p in all_permits if p.get(bin_column) in bins_set]
        # Option 2: Try padding to 7 digits
        bins_set_padded = {bin_val.zfill(7) for bin_val in bins_set}
        filtered_permits2 = [p for p in all_permits if p.get(bin_column) in bins_set_padded]
        
        logger.info(f"Matches found with original BINs: {len(filtered_permits1)}")
        logger.info(f"Matches found with padded BINs: {len(filtered_permits2)}")
        
        # Use the better matching approach
        filtered_permits = filtered_permits1 if len(filtered_permits1) >= len(filtered_permits2) else filtered_permits2
        
    else:
        filtered_permits = []
    
    logger.info(f"Found {len(filtered_permits)} permits matching your {len(bins_set)} BINs")
    
    # 5) Save to CSV
    if filtered_permits:
        df = pd.DataFrame.from_records(filtered_permits)
        df.to_csv("permits_last5yrs.csv", index=False)
        logger.info(f"✅ Saved permits_last5yrs.csv with {len(df)} permits")
        
        # Show a sample
        logger.info("\nSample data:")
        logger.info(df.head(3).to_string())
    else:
        logger.warning("No matching permits found!")

except Exception as e:
    logger.error(f"Error in Socrata query: {e}")
    import traceback
    logger.error(traceback.format_exc())