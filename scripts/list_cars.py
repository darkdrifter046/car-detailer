import os
import re
import sys

# Add scripts directory to Python path
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from config import MAIN_HTML, CAR_LIST_TXT

MAIN_FILE = MAIN_HTML

def get_all_titles():
    try:
        with open(MAIN_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("main.html not found")
        return

    # Split by brands similar to refactor.py
    parts = re.split(r'(<h1>.*?</h1>)', content, flags=re.DOTALL)
    
    total_cars = 0
    brand_counts = {}
    
    for i in range(1, len(parts), 2):
        h1_tag = parts[i]
        section_content = parts[i+1] if i+1 < len(parts) else ""
        
        clean_name = re.sub(r'<[^>]+>', '', h1_tag).strip()
        brand = clean_name.replace("Cars Collection", "").replace("Showcase", "").replace("Cars Gallery", "").replace("Gallery", "").replace("Cars", "").split("—")[0].strip()
        
        # Simple extraction of titles using one of the common patterns for quick estimation
        # We'll use a broad regex to capture potentially all titles identified in refactor logic
        # Pattern set from refactor.py:
        # div.car-title, div.model, h3.title, h2, h3
        
        titles = []
        
        # Re-using logic from refactor.py effectively
        # We basically need to use the SAME extraction logic to know exactly what we have
        
        # Let's just quick-scan for now
        t_matches = re.findall(r'<div class="car-title">(.*?)</div>', section_content)
        t_matches += re.findall(r'<div class="model">(.*?)</div>', section_content)
        t_matches += re.findall(r'<h3[^>]*class="title"[^>]*>(.*?)</h3>', section_content)
        t_matches += re.findall(r'<h2>(.*?)</h2>', section_content)
        t_matches += re.findall(r'<h3>(.*?)</h3>', section_content)
        
        # Clean duplicates or noise if any (rough set)
        clean_titles = []
        for t in t_matches:
            t = re.sub(r'<[^>]+>', '', t).strip()
            if t and t not in clean_titles:
                clean_titles.append(t)
                
        print(f"Brand: {brand} - Count: {len(clean_titles)}")
        # print(clean_titles[:3]) # Show first 3 samples
        total_cars += len(clean_titles)
        brand_counts[brand] = clean_titles

    print(f"\nTotal estimated cars: {total_cars}")
    
    # Save to a file for reference
    with open(CAR_LIST_TXT, "w") as f:
        for brand, models in brand_counts.items():
            f.write(f"=== {brand} ===\n")
            for m in models:
                f.write(f"{m}\n")
            f.write("\n")

if __name__ == "__main__":
    get_all_titles()
