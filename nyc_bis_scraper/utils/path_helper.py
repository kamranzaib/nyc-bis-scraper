"""
Path helper module to ensure imports work correctly regardless of where scripts are executed from.
"""

import os
import sys
from pathlib import Path


def add_project_root_to_path():
    """
    Add the project root directory to sys.path to ensure imports work correctly.
    This should be used in standalone scripts that need to be run directly.
    """
    # Get the current file's directory
    current_file = Path(os.path.abspath(__file__))
    
    # Navigate up to the project root (nyc-bis-scraper directory)
    project_root = current_file.parent.parent.parent
    
    # Add to sys.path if not already there
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"Added {project_root} to Python path")
    
    return project_root


def get_data_directory():
    """
    Get the path to the data directory.
    """
    project_root = Path(os.path.abspath(__file__)).parent.parent.parent
    data_dir = project_root / "data"
    
    # Create the directory if it doesn't exist
    if not data_dir.exists():
        data_dir.mkdir(parents=True)
    
    return data_dir


def get_output_directory():
    """
    Get the path to the outputs directory.
    """
    project_root = Path(os.path.abspath(__file__)).parent.parent.parent
    output_dir = project_root / "outputs"
    
    # Create the directory if it doesn't exist
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    
    return output_dir