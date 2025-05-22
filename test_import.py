
try:
    import nyc_bis_scraper
    print("\033[92mSuccess: Imported nyc_bis_scraper package!\033[0m")
    print(f"Package located at: {nyc_bis_scraper.__file__}")
    
    from nyc_bis_scraper.scripts.pipeline.run_pipeline import main
    print("\033[92mSuccess: Imported main function from pipeline!\033[0m")
    
    print("\nPackage is working correctly!")
except ImportError as e:
    print(f"\033[91mImport error: {e}\033[0m")
    
    import sys
    print("\nPython path:")
    for p in sys.path:
        print(f"  {p}")
