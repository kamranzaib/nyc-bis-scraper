"""
Test script to verify module imports are working correctly.
"""
try:
    print("Testing imports...")
    
    # Test imports directly from scripts module
    from scripts.extractors.footprints import fetch_footprints
    print("✅ Imported footprints")
    
    from scripts.extractors.pluto import fetch_pluto
    print("✅ Imported pluto")
    
    from scripts.extractors.permits import fetch_permits
    print("✅ Imported permits")
    
    from scripts.extractors.sales import fetch_sales
    print("✅ Imported sales")
    
    print("\nAll imports successful!")
except Exception as e:
    print(f"❌ Import error: {e}")