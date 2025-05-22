# Development Guide

## Installing in Development Mode

To install the package in development mode, follow these steps:

1. Navigate to the project root directory:
   ```bash
   cd /path/to/nyc-bis-scraper
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

This creates a symlink to your project, so changes you make to the code will be immediately available without reinstalling.

## Running Tests

To run tests:
```bash
python -m pytest tests/
```

## Using the Package

After installing in development mode, you can:

1. Import modules from anywhere:
   ```python
   from nyc_bis_scraper.scripts.extractors import permits
   ```

2. Run the CLI tool:
   ```bash
   nyc-bis-scraper
   ```

## Project Structure

```
nyc_bis_scraper/
├── __init__.py         # Package marker
├── run.py              # CLI entry point
└── scripts/            # Module code
    ├── __init__.py
    ├── extractors/     # Data extraction modules
    ├── analysis/       # Analysis modules
    ├── maps/           # Map generation modules
    ├── mergers/        # Data merging modules
    └── pipeline/       # Pipeline runner
```

## Common Issues

- If you get `ModuleNotFoundError` when running tests, make sure your PYTHONPATH includes the project root.
- For scripts that need to be run as standalone, use the helper module pattern described in the imports guide.