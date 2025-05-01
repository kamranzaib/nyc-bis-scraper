#!/usr/bin/env python
"""
NYC-BIS-SCRAPER main runner
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import the pipeline runner
from scripts.pipeline.run_pipeline import main

if __name__ == "__main__":
    main()
