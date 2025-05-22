# Imports Guide

This guide demonstrates how to properly import modules in your NYC BIS Scraper project.

## 1. Imports When Using the Installed Package

After installing the package (regular or development mode), you can import modules directly:

```python
# Import a module from the package
from nyc_bis_scraper.scripts.extractors import permits

# Import a specific function
from nyc_bis_scraper.scripts.extractors.permits import fetch_permits

# Import the path helper
from nyc_bis_scraper.utils.path_helper import get_data_directory

# Using the imported function
df = fetch_permits(last_n_days=30)
```

## 2. Imports When Running Scripts as Standalone

For scripts that need to run directly (not imported), use the path helper:

```python
#!/usr/bin/env python
"""
Example standalone script that can be run from any location
"""

# Add this at the top of any standalone script
import os
import sys
from pathlib import Path

# Add the project root to path (Method 1 - manual)
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
project_root = script_dir.parent  # Adjust the number of .parent calls as needed
sys.path.insert(0, str(project_root))

# Now you can import from the project
from nyc_bis_scraper.scripts.extractors import permits

# OR use our helper module (Method 2 - recommended)
from nyc_bis_scraper.utils.path_helper import add_project_root_to_path

# Add project root to path
add_project_root_to_path()

# Now import modules as needed
from nyc_bis_scraper.scripts.extractors import permits
```

## 3. Importing in Test Files

For test files:

```python
# test_example.py
import os
import sys
from pathlib import Path

# Add project root to path
current_file = Path(os.path.abspath(__file__))
project_root = current_file.parent.parent  # Assuming tests are in project_root/tests
sys.path.insert(0, str(project_root))

# Now import the module to test
from nyc_bis_scraper.scripts.extractors import permits

# Test functions
def test_fetch_permits():
    # Test code here
    pass
```

## 4. Practical Examples

### Example 1: Script in the project that imports other modules

```python
# File: nyc_bis_scraper/scripts/analysis/new_script.py

# Import from other modules in the package
from nyc_bis_scraper.scripts.extractors.permits import fetch_permits
from nyc_bis_scraper.scripts.extractors.pluto import fetch_pluto

def analyze_data():
    permits_df = fetch_permits()
    pluto_df = fetch_pluto()
    # Analysis code...

if __name__ == "__main__":
    analyze_data()
```

### Example 2: Standalone script outside the project

```python
# File: /some/other/location/analyze_nyc_data.py

# Add project to path
import os
import sys
from pathlib import Path

# Method 1: If the package is installed
from nyc_bis_scraper.utils.path_helper import add_project_root_to_path
add_project_root_to_path()

# Method 2: If the package is not installed but you know the path
nyc_bis_path = "/Users/kamranxeb/Desktop/nyc-bis-scraper"
if nyc_bis_path not in sys.path:
    sys.path.insert(0, nyc_bis_path)

# Now import what you need
from nyc_bis_scraper.scripts.extractors.permits import fetch_permits

# Your script code
def main():
    df = fetch_permits()
    print(f"Found {len(df)} permits")

if __name__ == "__main__":
    main()
```

### Example 3: Using relative imports within the package

```python
# File: nyc_bis_scraper/scripts/mergers/new_merger.py

# If you're importing from a parent or sibling package
from ..extractors.permits import fetch_permits
from ..extractors.pluto import fetch_pluto

# If you're importing from within the same package
from . import build_master

def merge_data():
    # Use imported functions
    permits_df = fetch_permits()
    # More code...
```

## Best Practices

1. **Install in Development Mode**: This is the easiest solution as it makes imports work correctly from anywhere.

2. **Use Absolute Imports**: When possible, use absolute imports starting with the package name:
   ```python
   from nyc_bis_scraper.scripts.extractors import permits
   ```

3. **For Standalone Scripts**: Use the path helper module:
   ```python
   from nyc_bis_scraper.utils.path_helper import add_project_root_to_path
   add_project_root_to_path()
   ```

4. **Consistent Data Paths**: For file paths, use the path helper functions:
   ```python 
   from nyc_bis_scraper.utils.path_helper import get_data_directory
   data_path = get_data_directory() / "permits.csv"
   ```