# Luxury Car Gallery

A beautiful, interactive showcase website displaying luxury car collections from the world's most prestigious brands.

## Project Structure

```
c/
├── scripts/              # Python generation scripts
│   ├── config.py        # Shared configuration and paths
│   ├── refactor.py      # Main HTML page generator
│   ├── enrich_data.py   # Car description data generator
│   ├── list_cars.py     # Car inventory listing utility
│   └── cleanup.py       # HTML cleanup utility
├── data/                 # Data files
│   └── descriptions.json        # Unified car data (descriptions + specs)
├── public/               # Generated website (served by HTTP server)
│   ├── home.html        # Brand selection homepage
│   ├── main.html        # Main source HTML template
│   ├── *.html           # Generated brand pages
│   └── style.css        # Stylesheet
├── car_list.txt         # Generated car inventory list
└── README.md            # This file
```

## Features

- **Interactive Car Cards**: Click any car to view detailed specifications and descriptions
- **Live Search**: Real-time search across all brands and models
- **Brand-Specific Pages**: Dedicated pages for each luxury brand with custom brand colors
- **Brand Color System**: Each brand page uses its authentic brand color (BMW Blue, Ferrari Red, etc.)
- **Rich Descriptions**: Curated descriptions for iconic models
- **Responsive Design**: Beautiful modern UI with glassmorphism and smooth animations
- **Smart Popups**: Complete car narratives with specifications in modal dialogs

## Quick Start

### 1. Generate the Website

Run the main generator to create all brand pages:

```bash
cd /Users/nikhilkaushik/Documents/c
python3 scripts/refactor.py
```

This will:
- Parse `public/main.html` to extract car data
- Generate individual brand pages in `public/`
- Create a unified search index
- Generate `public/home.html` with brand cards

### 2. Serve the Website Locally

Start a local HTTP server to view the site:

```bash
python3 -m http.server 8080 -d public
```

Then open your browser to: `http://localhost:8080/home.html`

## Available Scripts

### Regenerate HTML Pages
```bash
python3 scripts/refactor.py
```
Parses the main HTML and generates clean, optimized brand pages with search functionality.

### Update Car Descriptions
```bash
python3 scripts/enrich_data.py
```
Regenerates `data/descriptions.json` with curated car model descriptions.

### List All Cars
```bash
python3 scripts/list_cars.py
```
Generates `car_list.txt` with a complete inventory of all cars by brand.

### Clean Up HTML Files
```bash
python3 scripts/cleanup.py
```
Removes unwanted HTML files from the `public/` directory (use with caution).

## Data Files

### `data/descriptions.json`
Unified data file containing rich, curated descriptions and optional specifications for car models, organized by brand.

**Format:**
- **Most cars:** Simple string descriptions
- **Special cars:** Object format with `description` and `specs` fields for models requiring specification overrides (e.g., Bugatti Chiron, Ferrari LaFerrari, McLaren F1)

This single file serves as the centralized source for all car data, making it easy to maintain and update.

## Customization

### Adding a New Brand

1. Add car cards to `public/main.html` within a new `<h1>Brand Name</h1>` section
2. Add descriptions in `scripts/enrich_data.py` DATA dictionary
3. Run `python3 scripts/enrich_data.py` to update descriptions.json
4. Run `python3 scripts/refactor.py` to generate the new brand page

### Modifying Styles

Edit `public/style.css` to customize colors, layouts, and animations.

### Adding Brand Colors

Update the `BRAND_COLORS` dictionary in `scripts/refactor.py` to define accent colors for each brand.

## Requirements

- Python 3.6+
- No external dependencies (uses Python standard library only)

## Tips

- Always regenerate pages after updating `public/main.html`
- The HTTP server must serve from the `public/` directory
- Brand pages are auto-generated; edit `main.html` for content changes
- Search functionality works across all generated pages

## Recent Updates

### January 2026 - Brand Color System Fix
- **Fixed Heading Colors**: Removed hardcoded red color from CSS gradients
- **Brand-Specific Colors**: Each brand page now displays its authentic brand color:
  - BMW: BMW Blue (#0066B1)
  - Ferrari: Rosso Corsa (#FF2800)
  - Lamborghini: Verde Mantis (#78C02B)
  - Mercedes: Silver (#A5A5A5)
  - McLaren: McLaren Orange (#FF8000)
  - Porsche: Guards Red (#C20018)
  - Aston Martin: British Racing Green (#006E51)
  - Alfa Romeo: Rosso Alfa (#AA1122)
  - Bugatti: French Racing Blue (#0055AB)
  - Dodge: Plum Crazy Purple (#6A0DAD)
  - Koenigsegg: Orange/Yellow (#FEA304)
  - Maserati: Dark Blue (#0C2340)
- **CSS Improvements**: Simplified heading gradients while maintaining elegant underline fade effect

Enjoy exploring the world's most amazing cars! 🚗✨
