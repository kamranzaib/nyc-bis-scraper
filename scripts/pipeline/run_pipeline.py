#!/usr/bin/env python
"""
Dynamic pipeline runner for NYC-BIS-SCRAPER
Automatically discovers and runs scripts in the project
"""

import argparse
import yaml
import importlib.util
import os
import sys
from pathlib import Path

def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def find_all_scripts(base_dir):
    """Find all Python scripts in the given directories"""
    scripts = {}
    script_dirs = {
        "extractors": os.path.join(base_dir, "scripts", "extractors"),
        "mergers": os.path.join(base_dir, "scripts", "mergers"),
        "maps": os.path.join(base_dir, "scripts", "maps")
    }
    
    for category, dir_path in script_dirs.items():
        scripts[category] = []
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                if file.endswith('.py') and not file.startswith('__'):
                    script_name = file[:-3]  # Remove .py extension
                    script_path = os.path.join(dir_path, file)
                    scripts[category].append({
                        "name": script_name,
                        "path": script_path
                    })
    
    return scripts

def run_script(script_path, config):
    """Dynamically import and run a script with config"""
    print(f"Running: {os.path.basename(script_path)}")
    
    # Add script's directory to path
    script_dir = os.path.dirname(script_path)
    sys.path.insert(0, script_dir)
    
    # Import the script as a module
    module_name = os.path.basename(script_path).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Run the script's main function if available
    if hasattr(module, 'main'):
        try:
            module.main(config)
        except TypeError:
            # If main doesn't accept config, try without arguments
            try:
                module.main()
            except TypeError:
                print(f"Warning: Couldn't execute main() in {module_name}")
    else:
        # If no main function, the script was executed on import
        pass
    
    # Remove script dir from path to avoid conflicts
    if script_dir in sys.path:
        sys.path.remove(script_dir)

def list_available_scripts(scripts):
    """Print all available scripts"""
    print("\nAvailable scripts:")
    for category, script_list in scripts.items():
        if script_list:
            print(f"\n{category.upper()}:")
            for idx, script in enumerate(script_list, 1):
                print(f"  {idx}. {script['name']}")

def main():
    project_root = Path(__file__).parent.parent.parent
    all_scripts = find_all_scripts(project_root)
    config = load_config()
    
    parser = argparse.ArgumentParser(description="NYC BIS Scraper Pipeline")
    parser.add_argument('action', nargs='?', choices=['extract', 'merge', 'map', 'all', 'list'], 
                       default='list', help='Action to perform')
    parser.add_argument('--script', help='Run a specific script by name')
    parser.add_argument('--category', help='Run all scripts in a category')
    args = parser.parse_args()
    
    if args.action == 'list':
        list_available_scripts(all_scripts)
        return
    
    if args.script:
        # Find and run a specific script by name
        script_found = False
        for category, script_list in all_scripts.items():
            for script in script_list:
                if script['name'] == args.script:
                    run_script(script['path'], config)
                    script_found = True
                    break
            if script_found:
                break
        
        if not script_found:
            print(f"Script not found: {args.script}")
            list_available_scripts(all_scripts)
    
    elif args.category:
        # Run all scripts in a specific category
        if args.category in all_scripts:
            for script in all_scripts[args.category]:
                run_script(script['path'], config)
        else:
            print(f"Category not found: {args.category}")
            print(f"Available categories: {', '.join(all_scripts.keys())}")
    
    elif args.action == 'extract':
        for script in all_scripts.get('extractors', []):
            run_script(script['path'], config)
    
    elif args.action == 'merge':
        for script in all_scripts.get('mergers', []):
            run_script(script['path'], config)
    
    elif args.action == 'map':
        for script in all_scripts.get('maps', []):
            run_script(script['path'], config)
    
    elif args.action == 'all':
        # Run all scripts in the correct order
        for category in ['extractors', 'mergers', 'maps']:
            for script in all_scripts.get(category, []):
                run_script(script['path'], config)

if __name__ == "__main__":
    main()