
import os
import re

public_dir = r"C:\Users\Hp\Documents\Car\public"

# Pattern to find the specific style block related to search
# It usually starts after <link rel="stylesheet" href="style.css">
# And contains "/* Search Bar Styles */" or ".search-container"
# We will look for the <style>...</style> block that contains .search-container and remove it.

style_pattern = re.compile(r'<style>(\s|\S)*?\.search-container(\s|\S)*?</style>', re.MULTILINE)

for filename in os.listdir(public_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(public_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = style_pattern.sub('', content)
        
        # Also clean up any double empty lines left
        new_content = re.sub(r'\n\s*\n\s*\n', '\n\n', new_content)

        if content != new_content:
            print(f"Updating {filename}")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
        else:
            print(f"No changes in {filename}")

