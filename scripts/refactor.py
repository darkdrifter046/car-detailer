import os
import re
import json
import sys

# Add scripts directory to Python path if not already there
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from config import (
    PROJECT_ROOT, DATA_DIR, PUBLIC_DIR,
    MAIN_HTML, STYLE_CSS, DESCRIPTIONS_FILE,
    get_brand_html_path
)

# For backward compatibility with template generation
MAIN_FILE = MAIN_HTML
STYLE_FILE = "style.css"  # Relative path for HTML links

# Load Descriptions
DESCRIPTIONS = {}
try:
    with open(DESCRIPTIONS_FILE, "r", encoding="utf-8") as f:
        DESCRIPTIONS = json.load(f)
    print(f"Loaded {len(DESCRIPTIONS)} brands from descriptions.json")
except FileNotFoundError:
    print("Warning: descriptions.json not found. Using generic descriptions.")



# Iconic Brand Colors
BRAND_COLORS = {
    "Alfa Romeo": "#AA1122",   # Rosso Alfa (Deep Red)
    "Aston Martin": "#006E51", # British Racing Green
    "BMW": "#0066B1",          # BMW Blue
    "Bugatti": "#0055AB",      # French Racing Blue
    "Dodge": "#6A0DAD",        # Plum Crazy (Purple) for distinction
    "Ferrari": "#FF2800",      # Rosso Corsa (Bright Red)
    "Koenigsegg": "#FEA304",   # Orange/Yellow
    "Lamborghini": "#78C02B",  # Verde Mantis (Green)
    "Maserati": "#0C2340",     # Dark Blue
    "McLaren": "#FF8000",      # McLaren Orange
    "Mercedes": "#A5A5A5",     # Silver (Darkened for contrast)
    "Porsche": "#C20018",      # Guards Red
}

def escape_js_string(s):
    if not s: return ""
    return s.replace("\'", "\\\'").replace("\"", "&quot;").replace("\n", " ").replace("\r", "")

def clean_html_boilerplate(content, title, brand_name=None, search_index="[]"):
    # Determine accent color
    accent_color = "#d71e28" # Default
    if brand_name and brand_name in BRAND_COLORS:
        accent_color = BRAND_COLORS[brand_name]
        
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <link rel="stylesheet" href="{STYLE_FILE}">
    <style>
        :root {{
            --brand-color: {accent_color} !important;
        }}
        
        /* Search Bar Styles */
        .search-container {{
            position: fixed;
            top: 25px;
            left: 80px; /* Right of home icon */
            z-index: 100;
        }}
        
        .search-input {{
            width: 200px;
            height: 45px;
            padding: 0 15px 0 40px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            color: white;
            font-size: 16px;
            outline: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        
        .search-input::placeholder {{
            color: rgba(255, 255, 255, 0.6);
        }}
        
        .search-input:focus {{
            width: 300px;
            background: rgba(255, 255, 255, 0.15);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            border-color: rgba(255, 255, 255, 0.3);
        }}
        
        .search-icon {{
            position: absolute;
            top: 50%;
            left: 12px;
            transform: translateY(-50%);
            width: 18px;
            height: 18px;
            color: rgba(255, 255, 255, 0.6);
            pointer-events: none;
        }}
        
        .search-results {{
            position: absolute;
            top: 55px;
            left: 0;
            width: 100%;
            max-height: 300px;
            overflow-y: auto;
            background: rgba(30, 30, 30, 0.95);
            backdrop-filter: blur(15px);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            display: none;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        
        .search-result-item {{
            padding: 10px 15px;
            display: flex;
            align-items: center;
            cursor: pointer;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            transition: background 0.2s;
        }}
        
        .search-result-item:last-child {{
            border-bottom: none;
        }}
        
        .search-result-item:hover {{
            background: var(--brand-color);
        }}
        
        .search-result-img {{
            width: 40px;
            height: 40px;
            border-radius: 6px;
            object-fit: cover;
            margin-right: 12px;
        }}
        
        .search-result-text {{
            color: white;
            font-size: 14px;
        }}
    </style>
</head>
<body>

    <a href="home.html" class="nav-home" title="Back to Home">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
    </a>
    
    <div class="search-container">
        <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" class="search-input" placeholder="Search cars..." id="searchInput">
        <div class="search-results" id="searchResults"></div>
    </div>
    
    {content}

    <!-- Modal Structure -->
    <div id="carModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span class="modal-close" onclick="closeModal()">&times;</span>
                <div class="modal-image-container">
                    <img id="modalImg" src="" alt="Car Image">
                </div>
            </div>
            <div class="modal-body">
                <h2 id="modalTitle" class="modal-title"></h2>
                <div id="modalSpecs" class="modal-specs"></div>
                <div id="modalDesc" class="modal-description"></div>
            </div>
        </div>
    </div>

    <script>
        const GLOBAL_CARS = {search_index};
        
        const searchInput = document.getElementById('searchInput');
        const searchResults = document.getElementById('searchResults');
        
        searchInput.addEventListener('input', function(e) {{
            const query = e.target.value.toLowerCase();
            searchResults.innerHTML = '';
            
            if (query.length < 1) {{
                searchResults.style.display = 'none';
                return;
            }}
            
            const matches = GLOBAL_CARS.filter(car => 
                car.title.toLowerCase().includes(query)
            );
            
            if (matches.length > 0) {{
                searchResults.style.display = 'block';
                matches.slice(0, 8).forEach(car => {{ // Limit to 8 results
                    const div = document.createElement('div');
                    div.className = 'search-result-item';
                    
                    // Escape basic quotes for JS string
                    const sTitle = car.title.replace(/'/g, "\\'");
                    const sImg = car.image.replace(/'/g, "\\'");
                    const sDesc = car.description.replace(/'/g, "\\'").replace(/"/g, '&quot;');
                    
                    div.innerHTML = `
                        <img src="${{car.image}}" class="search-result-img">
                        <span class="search-result-text">${{car.title}}</span>
                    `;
                    
                    div.onclick = function() {{
                        // Open modal directly
                        openModal(sTitle, sImg, '', sDesc);
                        searchResults.style.display = 'none';
                        searchInput.value = '';
                    }};
                    
                    searchResults.appendChild(div);
                }});
            }} else {{
                searchResults.style.display = 'none';
            }}
        }});
        
        // Close search when clicking outside
        document.addEventListener('click', function(e) {{
            if (!document.querySelector('.search-container').contains(e.target)) {{
                searchResults.style.display = 'none';
            }}
        }});
        
        function openModal(title, image, specs, description) {{
            document.getElementById('modalTitle').innerText = title;
            document.getElementById('modalImg').src = image;
            document.getElementById('modalImg').alt = title;
            
            var specsDiv = document.getElementById('modalSpecs');
            specsDiv.innerHTML = specs;
            if (!specs) {{
                specsDiv.style.display = 'none';
            }} else {{
                specsDiv.style.display = 'block';
            }}
            
            document.getElementById('modalDesc').innerHTML = description;
            
            var modal = document.getElementById('carModal');
            modal.style.display = "block";
            document.body.style.overflow = "hidden"; // Prevent background scrolling
        }}

        function closeModal() {{
            var modal = document.getElementById('carModal');
            modal.style.display = "none";
            document.body.style.overflow = "auto";
        }}

        // Close when clicking outside
        window.onclick = function(event) {{
            var modal = document.getElementById('carModal');
            if (event.target == modal) {{
                closeModal();
            }}
        }}
    </script>
</body>
</html>"""

def generate_home_page(brands, search_index="[]"):
    cards_html = ""
    for brand in brands:
        if brand['count'] == 0:
            continue
            
        # Generate a unified card for the homepage
        cards_html += f"""
        <a class="car-card brand-card" href="{brand['filename']}">
            <img src="{brand['image']}" alt="{brand['name']}">
            <div class="car-info">
                <div class="car-title">{brand['name']}</div>
                <div class="specs">
                    {brand['count']} Models Available
                </div>
            </div>
        </a>
        """
    
    return clean_html_boilerplate(f"""
    <h1>Luxury Car Gallery</h1>
    <div class="container">
        {cards_html}
    </div>
    """, "Luxury Car Gallery | Home", brand_name="Home", search_index=search_index)

def smart_extract_card(content):
    """
    Tries to extract image, title, and specs from a snippet of HTML 
    using various known patterns.
    """
    # 1. Image (Universal)
    img_match = re.search(r'<img[^>]+src="([^"]+)"', content)
    img_src = img_match.group(1) if img_match else ""
    
    alt_match = re.search(r'<img[^>]+alt="([^"]+)"', content)
    img_alt = alt_match.group(1) if alt_match else "Car"

    # If no image, it's likely not a valid card chunk
    if not img_src:
        return None

    # 2. Title (Try multiple patterns in order of likelihood)
    title = "Unknown Model"
    
    title_res = [
        r'<div class="car-title">(.*?)</div>',      # Pattern A
        r'<div class="model">(.*?)</div>',          # Pattern B
        r'<h3[^>]*class="title"[^>]*>(.*?)</h3>',   # Pattern D (Mercedes)
        r'<h2>(.*?)</h2>',                          # Pattern C (Dodge)
        r'<h3>(.*?)</h3>',                          # Pattern E/F (Ferrari)
        r'<h3[^>]*>(.*?)</h3>'                      # Generic H3
    ]
    
    for r in title_res:
        m = re.search(r, content, re.DOTALL)
        if m:
            raw = m.group(1).strip()
            # Clean up badge spans or other tags inside title
            clean = re.sub(r'<span[^>]*>.*?</span>', '', raw).strip()
            # Remove HTML tags if any remain
            clean = re.sub(r'<[^>]+>', '', clean).strip()
            if clean:
                title = clean
                break

    # 3. Specs (Try multiple patterns)
    specs = ""
    
    # helper to extract balanced div content
    def extract_balanced(html, start_str):
        start_idx = html.find(start_str)
        if start_idx == -1: return None
        
        content_start = start_idx + len(start_str)
        open_tags = 1
        i = content_start
        
        while i < len(html):
            if html[i:i+4] == '<div':
                open_tags += 1
                i += 4
            elif html[i:i+6] == '</div>':
                open_tags -= 1
                if open_tags == 0:
                    return html[content_start:i].strip()
                i += 6
            else:
                i += 1
        return None

    # Pattern A/C with nested divs handling
    if '<div class="specs">' in content:
        # Try balanced extraction first
        specs = extract_balanced(content, '<div class="specs">')

    if not specs:
        specs_res = [
            r'<div class="specs">(.*?)</div>',          # Pattern A / C (Simple fallback)
            r'<p class="spec">(.*?)</p>',               # Pattern F (Ferrari)
            (r'<div class="meta">(.*?)</div>', True),   # Pattern D (Mercedes) - Multi match
            r'<p>(.*?)</p>',                            # Pattern G (BMW - Generic P)
        ]
        
        for item in specs_res:
            if isinstance(item, tuple):
                # Handler for multi-match (like Mercedes metas)
                r, multi = item
                matches = re.findall(r, content, re.DOTALL)
                if matches:
                    # Join them
                    specs = "<br/>".join([m.strip() for m in matches])
                    break
            else:
                r = item
                m = re.search(r, content, re.DOTALL)
                if m:
                    specs = m.group(1).strip()
                    break
    
    # Post-processing specs
    return {
        'image': img_src,
        'alt': img_alt,
        'title': title,
        'specs': specs,
        'raw_specs': specs  # Keep raw for parsing
    }

def extract_specs_data(specs_html):
    """
    Parses HTML specs into a structured dictionary.
    Handles <br>, newlines, and pipe (|) separators.
    Infers keys if missing based on units.
    """
    if not specs_html:
        return {}
        
    # Cleanup text
    # Replace common separators with newlines
    text = specs_html.replace("<br/>", "\n").replace("<br>", "\n").replace("·", "\n").replace("•", "\n").replace("|", "\n")
    text = re.sub(r'<[^>]+>', '', text)
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    kv_pairs = {}
    
    for line in lines:
        # 1. Try Key: Value
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip().lower()
            val = parts[1].strip()
            kv_pairs[key] = val
        else:
            # 2. Try to infer key from value unit
            val = line
            lower_val = val.lower()
            
            if 'hp' in lower_val or 'bhp' in lower_val or 'ps' in lower_val:
                kv_pairs['horsepower'] = val
            elif 'km/h' in lower_val or 'mph' in lower_val:
                # Distinguish accel from top speed? 
                # Accel usually has "0-100" but if that's missing...
                # Top speed usually just "300 km/h"
                if '0-100' in lower_val or '0–100' in lower_val or 'sec' in lower_val or re.search(r'\d+\.?\d*s$', lower_val):
                     kv_pairs['acceleration'] = val
                else:
                     kv_pairs['top speed'] = val
            elif '₹' in val or '$' in val or '€' in val or '£' in val or 'cr' in lower_val or 'lakh' in lower_val:
                kv_pairs['price'] = val
            elif re.search(r'\d+\.?\d*s$', lower_val): # Ends in 's' (e.g. 3.4s)
                kv_pairs['acceleration'] = val
    
            

    return kv_pairs

def get_normalized_specs(specs_data, brand_name, car_title):
    """
    Returns a normalized dictionary of specs with standard keys.
    Checks unified DESCRIPTIONS data structure for spec overrides.
    """
    data = specs_data.copy()
    
    # 1. Check unified DESCRIPTIONS for spec overrides
    # Find matching brand
    matched_brand_key = None
    for k in DESCRIPTIONS.keys():
        if k.lower() in brand_name.lower() or brand_name.lower() in k.lower():
            matched_brand_key = k
            break
    
    if matched_brand_key:
        models_db = DESCRIPTIONS[matched_brand_key]
        # Search for model match
        title_lower = car_title.lower()
        sorted_keys = sorted(models_db.keys(), key=len, reverse=True)
        
        for model_key in sorted_keys:
            if model_key.lower() in title_lower:
                model_data = models_db[model_key]
                # Check if it's an object with specs
                if isinstance(model_data, dict) and 'specs' in model_data:
                    data.update(model_data['specs'])
                break
    
    # 2. Normalize Keys
    key_map = {
        'horsepower': ['horsepower', 'power', 'output', 'hp'],
        'top speed': ['top speed', 'max speed', 'speed', 'top'],
        'price': ['price', 'base price', 'cost'],
        'acceleration': ['0–100 km/h', '0-100 km/h', '0-60 mph', '0-60', 'acceleration', '0-100', '0–100']
    }
    
    normalized = {}
    for target, variations in key_map.items():
        # First check if the standard key already exists
        if target in data:
            normalized[target] = data[target]
            continue
            
        # Then check variations
        for v in variations:
            if v in data:
                normalized[target] = data[v]
                break
                
    # Copy other keys too? No, strict format only cares about these 4.
    return normalized

def format_specs_strict(specs_data, brand_name, car_title):
    """
    Returns HTML string strictly following the user's template.
    Checks enrichment data for missing fields.
    """
    # 1. Normalize Data
    normalized = get_normalized_specs(specs_data, brand_name, car_title)
    
    # 4. Check for missing critical fields and log
    required_keys = ['horsepower', 'top speed', 'price', 'acceleration']
    missing = [k for k in required_keys if k not in normalized]
    
    if missing:
        print(f"[MISSING] {brand_name} | {car_title}: {', '.join(missing)}")
        
    # 5. Format Output
    # Handling specific formatting details (removing units if they are going to be added by template, or keeping them if varied)
    # The prompt asks for:
    # Horsepower: {} HP
    # Top Speed: {} km/h ({} mph)
    # Price: ₹{}
    # 0–100 km/h: {}s
    
    # We need to be careful not to double-add units if they are already in the source string.
    # Simple heuristic: strip the unit from the variable if present.
    
    def strip_unit(val, unit):
        if not val: return "?"
        return re.sub(f"\\s*{re.escape(unit)}.*", "", val, flags=re.IGNORECASE).strip()
    
    hp = strip_unit(normalized.get('horsepower', '?'), 'HP')
    
    speed_raw = normalized.get('top speed', '?')
    # Try to extract km/h and mph if possible, otherwise just dump raw
    # Expected: "330 km/h (205 mph)"
    speed_kmh = "?"
    speed_mph = "?"
    
    if 'km/h' in speed_raw:
        speed_kmh = strip_unit(speed_raw, 'km/h')
        if '(' in speed_raw and 'mph' in speed_raw:
             speed_mph = re.search(r'\((.*?)\s*mph\)', speed_raw).group(1).strip()
    elif 'mph' in speed_raw and 'km/h' not in speed_raw:
        # Check if we need to convert? For now just try to extract
        speed_mph = strip_unit(speed_raw, 'mph')
        
    price_raw = normalized.get('price', '?')
    # Assume price has symbol, try to strip it if it's not the requested one? 
    # Requested: ₹{}
    # Existing source might be "₹32,00,00,000" or "$2M"
    # We will just print the raw price for now, assuming source has ₹ usually. 
    # Actually user template says "Price: ₹{}". So I should strip '₹' if present.
    price = price_raw.replace('₹', '').strip()
    
    accel_raw = normalized.get('acceleration', '?')
    accel = strip_unit(accel_raw, 's')

    return f'''
        <b>Horsepower:</b> {hp} HP<br />
        <b>Top Speed:</b> {speed_kmh} km/h ({speed_mph} mph)<br />
        <b>Price:</b> ₹{price}<br />
        <b>0–100 km/h:</b> {accel}s
    '''.strip()

def get_description_for_car(brand_name, car_title):
    """
    Finds the best matching description for a car title within a brand's data.
    Handles both string descriptions (legacy) and object format with description+specs (new).
    """
    # Normalize title for search
    title_lower = car_title.lower()
    
    # Check if brand exists in DB
    matched_brand_key = None
    for k in DESCRIPTIONS.keys():
        if k.lower() in brand_name.lower() or brand_name.lower() in k.lower():
            matched_brand_key = k
            break
            
    if not matched_brand_key:
        return f"Explore the {car_title}, a testament to {brand_name}'s engineering."
        
    models_db = DESCRIPTIONS[matched_brand_key]
    
    # Fuzzy match: Look for model keywords in the car title
    # Sort keys by length (descending) to match "Giulia Quadrifoglio" before "Giulia"
    sorted_keys = sorted(models_db.keys(), key=len, reverse=True)
    
    for model_key in sorted_keys:
        if model_key.lower() in title_lower:
            model_data = models_db[model_key]
            # Handle both string (legacy) and object (new) formats
            if isinstance(model_data, dict):
                return model_data.get('description', f"The {car_title} is a distinguished model from {brand_name}'s lineup.")
            else:
                # String format
                return model_data
            
    # Fallback to generic if no specific model matched
    return f"The {car_title} is a distinguished model from {brand_name}'s lineup, offering exceptional design and performance."

def parse_specs_to_narrative(specs_html):
    """
    Parses the HTML specs string into a natural language sentence.
    Expected format often includes key-value like "Power: 100hp".
    """
    if not specs_html:
        return ""
    
    # DEBUG PRINT
    print(f"DEBUG: Parsing specs: {specs_html!r}")
        
    # Strip HTML tags but keep structure for parsing
    # Typically parts are separated by <br/> or newlines
    text = specs_html.replace("<br/>", "\n").replace("<br>", "\n").replace("·", "\n").replace("•", "\n")
    # Remove other tags
    text = re.sub(r'<[^>]+>', '', text)
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    print(f"DEBUG: Extracted lines: {lines}")
    
    kv_pairs = {}
    
    # Try to parse properties
    # Common keys: Horsepower, Power, Output, Top Speed, 0-100, 0-60, Price, Engine
    for line in lines:
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip()
            val = parts[1].strip()
            kv_pairs[key.lower()] = val
    
    print(f"DEBUG: Pairs found: {kv_pairs}")
            
    if not kv_pairs:
        # If we couldn't parse structured data, just return the text as a sentence
        # cleanup double spaces
        clean_text = ". ".join(lines) + "."
        return f"Specifications: {clean_text}"

    # Construct narrative
    narrative_parts = []
    
    # Power
    power = kv_pairs.get('horsepower') or kv_pairs.get('power') or kv_pairs.get('output')
    if power:
        narrative_parts.append(f"It generates {power}")
        
    # Speed
    speed = kv_pairs.get('top speed') or kv_pairs.get('max speed')
    if speed:
        verb = "reaches a top speed of" if narrative_parts else "This vehicle reaches a top speed of"
        narrative_parts.append(f"{verb} {speed}")
        
    # Acceleration
    accel = kv_pairs.get('0–100 km/h') or kv_pairs.get('0-100 km/h') or kv_pairs.get('0-60 mph') or kv_pairs.get('acceleration')
    if accel:
        verb = "accelerates" if narrative_parts else "It accelerates"
        narrative_parts.append(f"{verb} from 0-100 km/h in {accel}")
        
    # Price
    price = kv_pairs.get('price') or kv_pairs.get('base price')
    if price:
        verb = "is available for" if narrative_parts else "This vehicle is available for"
        narrative_parts.append(f"{verb} {price}")
        
    if not narrative_parts:
         return f"Specifications: {', '.join(lines)}."
         
    # Join nicely
    # "It generates 630 HP, reaches a top speed of ..., and is available for ..."
    if len(narrative_parts) == 1:
        return narrative_parts[0] + "."
    elif len(narrative_parts) == 2:
        return " and ".join(narrative_parts) + "."
    else:
        return ", ".join(narrative_parts[:-1]) + ", and " + narrative_parts[-1] + "."



def process_brand_content(h1_tag, raw_content):
    # Remove specific JS blocks or script tags to avoid checking template strings
    raw_content = re.sub(r'<script.*?>.*?</script>', '', raw_content, flags=re.DOTALL)

    # Extract clean name
    clean_name = re.sub(r'<[^>]+>', '', h1_tag).strip()
    # Remove "30 Models" or similar patterns first
    clean_name = re.sub(r'\d+\s*Models?', '', clean_name, flags=re.IGNORECASE)
    
    short_name = clean_name.replace("Cars Collection", "").replace("Showcase", "").replace("Cars Gallery", "").replace("Gallery", "").replace("Cars", "").split("—")[0].strip()
    
    cards_data = []
    
    # Strategy: Find chunks that look like cards using various wrappers
    
    # Priority 1: <article class="card"> (Mercedes)
    articles = re.findall(r'(<article\s+class="card".*?>.*?</article>)', raw_content, re.DOTALL)
    if articles:
        print(f"DEBUG [{short_name}]: Strategy 1 (Article) matched {len(articles)}")
        for c in articles:
            data = smart_extract_card(c)
            if data: cards_data.append(data)
    
    # Priority 2: <a class="car-card"> (Alfa, Bugatti, etc)
    if not cards_data:
        anchors_car_card = re.findall(r'(<a\s+class="car-card".*?>.*?</a>)', raw_content, re.DOTALL)
        if anchors_car_card:
            print(f"DEBUG [{short_name}]: Strategy 2 (a.car-card) matched {len(anchors_car_card)}")
            for c in anchors_car_card:
                data = smart_extract_card(c)
                if data: cards_data.append(data)

    # Priority 3: <a class="card"> (Dodge)
    if not cards_data:
        anchors_card = re.findall(r'(<a\s+class="card".*?>.*?</a>)', raw_content, re.DOTALL)
        if anchors_card:
            print(f"DEBUG [{short_name}]: Strategy 3 (a.card) matched {len(anchors_card)}")
            for c in anchors_card:
                data = smart_extract_card(c)
                if data: cards_data.append(data)

    # Priority 4: <div class="card"> (Aston, Ferrari)
    if not cards_data:
        parts = re.split(r'<div\s+class="card"', raw_content)
        if len(parts) > 1:
            print(f"DEBUG [{short_name}]: Strategy 4 (div.card split) matched {len(parts)-1} parts")
            for part in parts[1:]:
                chunk = part[:1000000]
                data = smart_extract_card(chunk)
                if data: cards_data.append(data)

    # Priority 5: Loose Items (BMW?)
    if not cards_data:
        loose_matches = re.findall(r'(<img[^>]+>\s*.*?<h[23][^>]*>.*?</h[23]>)', raw_content, re.DOTALL)
        if loose_matches:
            print(f"DEBUG [{short_name}]: Strategy 5 (Loose) matched {len(loose_matches)}")
            for c in loose_matches:
                data = smart_extract_card(c)
                if data: cards_data.append(data)

    cleaned_cards_html = ""
    first_image = ""
    
    for i, data in enumerate(cards_data):
        if i == 0: first_image = data['image']
        
        # Prepare safe strings for JS
        s_title = escape_js_string(data['title'])
        s_img = escape_js_string(data['image'])
        
        # 1. Parse Specs Data
        raw_specs_data = extract_specs_data(data.get('raw_specs', ''))
        
        # 2. Normalize Specs (Shared logic for formatting AND narrative)
        specs_data = get_normalized_specs(raw_specs_data, short_name, data['title'])
        
        # 3. Format Strictly (HTML for card)
        formatted_specs_html = format_specs_strict(raw_specs_data, short_name, data['title'])
        
        # 4. Create Narrative for Modal
        rich_desc = get_description_for_car(short_name, data['title'])
        
        # Generate narrative from structured data for the modal description
        narrative_parts = []
        if 'horsepower' in specs_data: narrative_parts.append(f"It generates {specs_data['horsepower']}")
        
        if 'top speed' in specs_data: 
             verb = "reaches a top speed of" if narrative_parts else "It reaches a top speed of"
             narrative_parts.append(f"{verb} {specs_data['top speed']}")
             
        if 'acceleration' in specs_data: 
             verb = "accelerates" if narrative_parts else "It accelerates"
             narrative_parts.append(f"{verb} from 0-100 km/h in {specs_data['acceleration']}")
             
        if 'price' in specs_data: 
             verb = "is available for" if narrative_parts else "It is available for"
             narrative_parts.append(f"{verb} {specs_data['price']}")
        
        narrative_text = ""
        if narrative_parts:
            narrative_text = ", ".join(narrative_parts) + "."
            
        full_desc = f"{rich_desc} <br/><br/>{narrative_text}" if narrative_text else rich_desc
        s_desc = escape_js_string(full_desc)
        
        # Enrich data object for global search index
        data['enriched_description'] = s_desc

        # Pass empty string for specs arg in modal to avoid duplication, specs now in description
        cleaned_cards_html += f"""
        <div class="car-card" onclick="openModal('{s_title}', '{s_img}', '', '{s_desc}')">
            <img src="{data['image']}" alt="{data['alt']}">
            <div class="car-info">
                <div class="car-title">{data['title']}</div>
                <div class="specs">
                    {formatted_specs_html}
                </div>
            </div>
        </div>
        """

    return short_name, cleaned_cards_html, first_image, cards_data

def main():
    try:
        with open(MAIN_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {MAIN_FILE} not found.")
        return

    # Splitting by "<h1>" to get sections
    parts = re.split(r'(<h1.*?>.*?</h1>)', content, flags=re.DOTALL)
    
    brands = []
    
    # Process sections
    brand_pages = []
    global_cars = []

    for i in range(1, len(parts), 2):
        h1_tag = parts[i]
        section_content = parts[i+1] if i+1 < len(parts) else ""
        
        name, cards_html, image, brand_cars = process_brand_content(h1_tag, section_content)
        count = len(brand_cars)
        
        brand_pages.append({
            "name": name,
            "filename": name.lower().replace(" ", "_").replace("-", "_") + ".html",
            "image": image,
            "count": count,
            "cards_html": cards_html
        })

        if count > 0:
            for car in brand_cars:
                # Add to global index
                global_cars.append({
                    "title": car['title'],
                    "image": car['image'],
                    "description": car.get('enriched_description', ''),
                    # We don't necessarily need 'specs' here if description is enriched
                })
        
        # Debug output
        if count == 0:
            print(f"Warning: No cars found for {name}")

    import json
    all_cars_json = json.dumps(global_cars)
    
    brands_for_home = []

    # Write files
    for brand in brand_pages:
        page_body = f"""
        <h1>{brand['name']}</h1>
        <div class="container">
            {brand['cards_html']}
        </div>
        """
        
        with open(get_brand_html_path(brand['name']), "w", encoding="utf-8") as f:
            f.write(clean_html_boilerplate(page_body, f"{brand['name']} | Luxury Car Gallery", brand_name=brand['name'], search_index=all_cars_json))
            
        print(f"Refactored {brand['filename']} with {brand['count']} cars.")
        
        brands_for_home.append({
            "name": brand['name'],
            "filename": brand['filename'],
            "image": brand['image'],
            "count": brand['count']
        })

    # Sort brands alphabetically
    brands_for_home.sort(key=lambda x: x["name"])

    # Generate Home Page
    from config import HOME_HTML
    with open(HOME_HTML, "w", encoding="utf-8") as f:
        f.write(generate_home_page(brands_for_home, search_index=all_cars_json))
    print("Regenerated home.html")

if __name__ == "__main__":
    main()
