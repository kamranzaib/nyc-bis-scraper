#!/usr/bin/env python
"""
This script performs additional cleanup on the NYC-BIS-SCRAPER project structure.
Run this from the project root directory after running the main restructure.py script.
"""

import os
import shutil
from pathlib import Path

# Define project root
PROJECT_ROOT = Path.cwd()

def cleanup_root_files():
    """Move stray files from root to their proper locations"""
    
    # Files to move: source -> destination
    moves = [
        {"from": "dob_permits_since_2020.jsonl", "to": "data/raw/permits/dob_permits_since_2020.jsonl"},
        {"from": "final_properties.csv", "to": "data/processed/final_properties.csv"}
    ]
    
    for move in moves:
        source = PROJECT_ROOT / move["from"]
        target = PROJECT_ROOT / move["to"]
        
        if source.exists():
            # Make sure target directory exists
            os.makedirs(os.path.dirname(target), exist_ok=True)
            
            # Only move if the target doesn't exist or is different
            if not target.exists() or os.path.getsize(source) != os.path.getsize(target):
                try:
                    shutil.move(str(source), str(target))
                    print(f"Moved: {move['from']} → {move['to']}")
                except Exception as e:
                    print(f"Error moving {move['from']}: {e}")
            else:
                # Remove source if target already exists and is identical
                os.remove(source)
                print(f"Removed duplicate file: {move['from']} (already exists at {move['to']})")
        else:
            print(f"Info: Source file not found: {move['from']}")

def promote_outputs_directory():
    """Move outputs directory from scripts/maps to project root"""
    
    # Paths
    source_html = PROJECT_ROOT / "scripts/maps/outputs/html"
    source_logs = PROJECT_ROOT / "scripts/maps/outputs/logs"
    source_outputs = PROJECT_ROOT / "scripts/maps/outputs"
    
    target_html = PROJECT_ROOT / "outputs/html"
    target_logs = PROJECT_ROOT / "outputs/logs"
    
    # Create target directories
    os.makedirs(target_html, exist_ok=True)
    os.makedirs(target_logs, exist_ok=True)
    
    # Move HTML files
    if source_html.exists():
        for file in source_html.glob("*"):
            target_file = target_html / file.name
            if not target_file.exists():
                try:
                    shutil.move(str(file), str(target_file))
                    print(f"Moved: {file.relative_to(PROJECT_ROOT)} → outputs/html/{file.name}")
                except Exception as e:
                    print(f"Error moving {file.name}: {e}")
    
    # Move log files
    if source_logs.exists():
        for file in source_logs.glob("*"):
            target_file = target_logs / file.name
            if not target_file.exists():
                try:
                    shutil.move(str(file), str(target_file))
                    print(f"Moved: {file.relative_to(PROJECT_ROOT)} → outputs/logs/{file.name}")
                except Exception as e:
                    print(f"Error moving {file.name}: {e}")
    
    # Remove the now-empty outputs directory in scripts/maps
    if source_outputs.exists():
        try:
            shutil.rmtree(source_outputs)
            print(f"Removed directory: scripts/maps/outputs/")
        except Exception as e:
            print(f"Error removing scripts/maps/outputs/: {e}")

def remove_legacy_files():
    """Remove files that have been replaced by versions in scripts/extractors"""
    
    # Files to remove
    legacy_files = [
        "scraper.py",  # Replaced by scripts/extractors/scraper.py
    ]
    
    # Archive directory (if you decide to archive instead of delete)
    archive_dir = PROJECT_ROOT / "archive"
    
    # Check if we should archive or delete
    archive_mode = False  # Set to True if you want to archive instead of delete
    
    if archive_mode:
        os.makedirs(archive_dir, exist_ok=True)
    
    # Process each file
    for file in legacy_files:
        file_path = PROJECT_ROOT / file
        
        if file_path.exists():
            if archive_mode:
                # Move to archive
                try:
                    shutil.move(str(file_path), str(archive_dir / file_path.name))
                    print(f"Archived: {file} → archive/{file_path.name}")
                except Exception as e:
                    print(f"Error archiving {file}: {e}")
            else:
                # Delete
                try:
                    os.remove(file_path)
                    print(f"Removed: {file}")
                except Exception as e:
                    print(f"Error removing {file}: {e}")
        else:
            print(f"Info: Legacy file not found: {file}")

def create_gitignore():
    """Create a useful .gitignore file"""
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# Jupyter Notebook
.ipynb_checkpoints

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS specific
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
outputs/html/*.html
*.log
"""
    
    gitignore_path = PROJECT_ROOT / ".gitignore"
    
    # Only create if it doesn't exist
    if not gitignore_path.exists():
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content)
        print("Created: .gitignore")
    else:
        print("Info: .gitignore already exists")

def main():
    print("Starting additional project cleanup...")
    
    # Run cleanup tasks
    cleanup_root_files()
    promote_outputs_directory()
    remove_legacy_files()
    create_gitignore()
    
    # Clean up empty directories
    print("\nRemoving empty directories...")
    for root, dirs, files in os.walk(PROJECT_ROOT, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path) and "venv" not in dir_path:
                try:
                    os.rmdir(dir_path)
                    print(f"Removed empty directory: {os.path.relpath(dir_path, PROJECT_ROOT)}")
                except:
                    pass  # Directory not empty or permission error
    
    print("\nProject cleanup complete!")
    print("\nYour project should now have a clean structure following best practices.")
    print("Don't forget to update imports in your Python files if needed.")

if __name__ == "__main__":
    main()