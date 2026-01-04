import os
import sys

# Add scripts directory to Python path
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from config import PUBLIC_DIR

# Files that MUST be kept
KEEP_FILES = {
    "main.html",
    "home.html",
    "style.css",
    # Brand Pages
    "alfa_romeo.html",
    "aston_martin.html",
    "dodge.html",
    "ferrari.html",
    "lamborghini.html",
    "maserati.html",
    "mclaren.html",
    "mercedes.html",
    "porsche.html",
    "bmw.html",
    "bugatti.html",
    "koenigsegg.html"
}

BASE_DIR = PUBLIC_DIR  # Clean files in public directory

def cleanup():
    deleted_count = 0
    kept_count = 0
    
    files = os.listdir(BASE_DIR)
    
    for f in files:
        if not f.endswith(".html"):
            continue
            
        if f in KEEP_FILES:
            kept_count += 1
            print(f"KEEPING: {f}")
        else:
            # It's an html file not in our allow list
            full_path = os.path.join(BASE_DIR, f)
            try:
                os.remove(full_path)
                # print(f"DELETED: {f}")
                deleted_count += 1
            except Exception as e:
                print(f"ERROR deleting {f}: {e}")

    print(f"\nCleanup Complete.")
    print(f"Deleted: {deleted_count} files")
    print(f"Kept: {kept_count} files")

if __name__ == "__main__":
    cleanup()
