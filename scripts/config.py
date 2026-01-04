"""
Shared configuration for car showcase generation scripts.
Centralizes all path definitions to avoid hardcoding across multiple files.
"""

import os

# Project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Main directories
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
PUBLIC_DIR = os.path.join(PROJECT_ROOT, "public")

# Data files
DESCRIPTIONS_FILE = os.path.join(DATA_DIR, "descriptions.json")

# Public/output files
MAIN_HTML = os.path.join(PUBLIC_DIR, "main.html")
HOME_HTML = os.path.join(PUBLIC_DIR, "home.html")
STYLE_CSS = os.path.join(PUBLIC_DIR, "style.css")

# Utility output
CAR_LIST_TXT = os.path.join(PROJECT_ROOT, "car_list.txt")

# Brand HTML output helper
def get_brand_html_path(brand_name):
    """
    Returns the path for a brand's HTML file.
    Example: get_brand_html_path("Alfa Romeo") -> "/path/to/public/alfa_romeo.html"
    """
    filename = brand_name.lower().replace(" ", "_") + ".html"
    return os.path.join(PUBLIC_DIR, filename)
