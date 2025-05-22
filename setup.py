from setuptools import setup, find_packages
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
