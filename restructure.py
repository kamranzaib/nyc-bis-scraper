#!/usr/bin/env python
"""
NYC-BIS-SCRAPER Project Restructure Script
This script converts the project to a proper Python package structure.
Run this from the project root directory.
"""

import os
import shutil
import sys
from pathlib import Path

# Define project root
PROJECT_ROOT = Path.cwd()

def create_package_structure():
    """Create the proper package structure"""
    print("Creating package structure...")
    
    # Create main package directory if it doesn't exist
    package_dir = PROJECT_ROOT / "nyc_bis_scraper"
    os.makedirs(package_dir, exist_ok=True)
    
    # Create __init__.py in package directory
    with open(package_dir / "__init__.py", 'w') as f:
        f.write('"""NYC BIS Scraper package."""\n')
    
    # Move scripts directory into package if it's not already there
    scripts_source = PROJECT_ROOT / "scripts"
    scripts_target = package_dir / "scripts"
    
    if scripts_source.exists() and not scripts_target.exists():
        print(f"Moving scripts directory to {scripts_target}")
        shutil.move(str(scripts_source), str(scripts_target))
    elif scripts_source.exists() and scripts_target.exists():
        print("Both source and target scripts directories exist. Merging...")
        # Copy files from source to target instead of moving the directory
        for item in scripts_source.glob('**/*'):
            relative_path = item.relative_to(scripts_source)
            target_path = scripts_target / relative_path
            
            if item.is_dir():
                os.makedirs(target_path, exist_ok=True)
            else:
                os.makedirs(target_path.parent, exist_ok=True)
                if not target_path.exists():
                    shutil.copy2(str(item), str(target_path))
        # Remove the original scripts directory
        shutil.rmtree(scripts_source)
    
    # Create __init__.py files in all subdirectories of scripts
    for dirpath, dirnames, filenames in os.walk(scripts_target):
        dirpath = Path(dirpath)
        init_file = dirpath / "__init__.py"
        if not init_file.exists():
            with open(init_file, 'w') as f:
                f.write('"""NYC BIS Scraper module."""\n')
            print(f"Created {init_file.relative_to(PROJECT_ROOT)}")

    # Create etl directory structure at project root
    etl_dir = PROJECT_ROOT / "etl"
    subdirs = ["extract", "transform", "load", "pipeline"]
    for subdir in subdirs:
        subdir_path = etl_dir / subdir
        os.makedirs(subdir_path, exist_ok=True)
        init_file = subdir_path / "__init__.py"
        if not init_file.exists():
            with open(init_file, 'w') as f:
                f.write(f'"""ETL {subdir} module."""\n')
            print(f"Created {init_file.relative_to(PROJECT_ROOT)}")
    # Create __init__.py in etl root folder
    etl_init = etl_dir / "__init__.py"
    if not etl_init.exists():
        with open(etl_init, 'w') as f:
            f.write('"""ETL package."""\n')
        print(f"Created {etl_init.relative_to(PROJECT_ROOT)}")

    # Create main run.py in the package
    run_py_path = package_dir / "run.py"
    if not run_py_path.exists():
        with open(run_py_path, 'w') as f:
            f.write('''#!/usr/bin/env python
"""
NYC-BIS-SCRAPER main runner
"""

from nyc_bis_scraper.scripts.pipeline.run_pipeline import main

def run():
    """Entry point for the application"""
    main()

if __name__ == "__main__":
    run()
''')
        print(f"Created {run_py_path.relative_to(PROJECT_ROOT)}")
    
    # Create launcher run.py in project root
    root_run_py = PROJECT_ROOT / "run.py"
    if not root_run_py.exists():
        with open(root_run_py, 'w') as f:
            f.write('''#!/usr/bin/env python
"""
NYC-BIS-SCRAPER main runner (launcher)
"""

from nyc_bis_scraper.run import run

if __name__ == "__main__":
    run()
''')
        print(f"Created {root_run_py.relative_to(PROJECT_ROOT)}")

def create_setup_py():
    """Create or update setup.py"""
    print("Creating setup.py...")
    
    setup_py_path = PROJECT_ROOT / "setup.py"
    
    with open(setup_py_path, 'w') as f:
        f.write('''from setuptools import setup, find_packages
import os

# Read requirements from requirements.txt if it exists
requirements = []
if os.path.exists('requirements.txt'):
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()

setup(
    name="nyc-bis-scraper",
    version="0.1.0",
    packages=find_packages(),
    description="NYC BIS Scraper Tool",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "nyc-bis-scraper=nyc_bis_scraper.run:run",
        ],
    },
)
''')
    print(f"Created {setup_py_path.relative_to(PROJECT_ROOT)}")

def fix_imports():
    """Fix imports in Python files"""
    print("Fixing imports in Python files...")
    
    package_dir = PROJECT_ROOT / "nyc_bis_scraper"
    
    # Get all Python files in the package
    py_files = list(package_dir.glob('**/*.py'))
    
    for py_file in py_files:
        with open(py_file, 'r') as f:
            content = f.read()
        
        # Skip __init__.py files
        if py_file.name == "__init__.py":
            continue
        
        # Replace old imports with new package-based imports
        modified_content = content
        
        # Fix imports from scripts.*
        modified_content = modified_content.replace(
            'from scripts.', 'from nyc_bis_scraper.scripts.')
        modified_content = modified_content.replace(
            'import scripts.', 'import nyc_bis_scraper.scripts.')
        
        # Fix imports from etl.*
        modified_content = modified_content.replace(
            'from etl.', 'from etl.')
        modified_content = modified_content.replace(
            'import etl.', 'import etl.')
        
        # If content was modified, write it back
        if modified_content != content:
            with open(py_file, 'w') as f:
                f.write(modified_content)
            print(f"Fixed imports in {py_file.relative_to(PROJECT_ROOT)}")

def install_package():
    """Install the package in development mode"""
    print("Installing package in development mode...")
    
    try:
        # Uninstall existing package first
        os.system(f"{sys.executable} -m pip uninstall -y nyc-bis-scraper")
        
        # Install in development mode
        os.system(f"{sys.executable} -m pip install -e .")
        print("Package installed successfully!")
    except Exception as e:
        print(f"Error installing package: {e}")

def cleanup_project():
    """Perform additional project cleanup"""
    print("Performing project cleanup...")
    
    # Clean up egg-info
    for item in PROJECT_ROOT.glob('*.egg-info'):
        shutil.rmtree(item)
        print(f"Removed {item.name}")
    
    # Create gitignore if it doesn't exist
    gitignore_path = PROJECT_ROOT / ".gitignore"
    if not gitignore_path.exists():
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
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content)
        print("Created .gitignore")

    # Create .env file with PYTHONPATH
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        with open(env_path, 'w') as f:
            f.write(f"PYTHONPATH={PROJECT_ROOT}\n")
        print("Created .env file with PYTHONPATH set to project root")
        print("Remember to source the .env file before running your project, e.g.:")
        print("  source .env")

def test_package():
    """Test the package installation"""
    print("Testing package installation...")
    
    test_script = PROJECT_ROOT / "test_import.py"
    with open(test_script, 'w') as f:
        f.write('''
try:
    import nyc_bis_scraper
    print("\\033[92mSuccess: Imported nyc_bis_scraper package!\\033[0m")
    print(f"Package located at: {nyc_bis_scraper.__file__}")
    
    from nyc_bis_scraper.scripts.pipeline.run_pipeline import main
    print("\\033[92mSuccess: Imported main function from pipeline!\\033[0m")
    
    print("\\nPackage is working correctly!")
except ImportError as e:
    print(f"\\033[91mImport error: {e}\\033[0m")
    
    import sys
    print("\\nPython path:")
    for p in sys.path:
        print(f"  {p}")
''')
    
    # Run the test script
    print("\nRunning import test...")
    os.system(f"{sys.executable} {test_script}")

def main():
    print("=" * 80)
    print("NYC-BIS-SCRAPER Project Restructure Script")
    print("=" * 80)
    print("This script will convert your project to a proper Python package.")
    print("Current directory:", PROJECT_ROOT)
    print("=" * 80)
    
    input("Press Enter to continue (Ctrl+C to cancel)...")
    
    # Execute restructuring steps
    create_package_structure()
    create_setup_py()
    fix_imports()
    cleanup_project()
    install_package()
    test_package()
    
    print("\n" + "=" * 80)
    print("Project restructuring complete!")
    print("=" * 80)
    print("Your project is now organized as a proper Python package.")
    print("You can run your project using:")
    print("  - python run.py")
    print("  - nyc-bis-scraper (if Python scripts directory is in your PATH)")
    print("=" * 80)

if __name__ == "__main__":
    main()