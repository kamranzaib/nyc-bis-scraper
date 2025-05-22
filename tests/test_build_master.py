#!/usr/bin/env python
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Create a mock version of the functions to avoid the need for actual data files
from scripts.mergers.build_master import build_master
import pandas as pd

# Create mock data for testing
mock_config = {
    'paths': {
        'raw_data': './data/raw',
        'processed_data': './data/processed',
        'outputs': './outputs'
    }
}

# Monkey patch the fetch functions to return empty DataFrames
from scripts.extractors import footprints, pluto, permits, sales

def mock_fetch_footprints():
    print("Using mock footprints data")
    return pd.DataFrame({'BIN': ['1', '2'], 'BBL': ['1', '2'], 'geometry': [None, None]})

def mock_fetch_pluto():
    print("Using mock PLUTO data")
    return pd.DataFrame({'BBL': ['1', '2'], 'Address': ['123 Main St', '456 Elm St']})

def mock_fetch_permits():
    print("Using mock permits data")
    return pd.DataFrame({'BIN': ['1', '2'], 'permit_type': ['NB', 'A1']})

def mock_fetch_sales():
    print("Using mock sales data")
    return pd.DataFrame({'BIN': ['1', '2'], 'price': [1000000, 2000000]})

# Replace the actual functions with our mocks
footprints.fetch_footprints = mock_fetch_footprints
pluto.fetch_pluto = mock_fetch_pluto
permits.fetch_permits = mock_fetch_permits
sales.fetch_sales = mock_fetch_sales

# Run build_master with our mock config
print("Running build_master with mock data...")
build_master(mock_config)
print("\nDone! Check the output CSV files.")