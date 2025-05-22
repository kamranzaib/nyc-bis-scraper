#!/usr/bin/env python
import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    # Try importing from scripts.extractors
    from scripts.extractors import permits
    print("✅ Successfully imported permits module from scripts.extractors")
except ImportError as e:
    print(f"❌ Error importing permits: {e}")

try:
    # Try importing from scripts.mergers
    from scripts.mergers import build_master
    print("✅ Successfully imported build_master module from scripts.mergers")
except ImportError as e:
    print(f"❌ Error importing build_master: {e}")

print("\nPython path:")
for p in sys.path:
    print(f"  - {p}")