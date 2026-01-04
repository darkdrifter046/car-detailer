# Luxury Car Gallery

A beautiful, interactive showcase website displaying luxury car collections from the world's most prestigious brands.

## Overview

This repository contains the generated static website for the Luxury Car Gallery. The project features a modern, responsive design with glassmorphism effects, smooth animations, and dedicated pages for various luxury car brands.

## Features

- **Interactive Car Cards**: Click any car to view detailed specifications and descriptions.
- **Live Search**: Real-time search across all brands and models.
- **Brand-Specific Pages**: Dedicated pages for each luxury brand with custom brand colors.
- **Brand Color System**: Each brand page features its authentic brand color (BMW Blue, Ferrari Red, etc.).
- **Rich Descriptions**: Curated descriptions for iconic models.
- **Responsive Design**: Beautiful modern UI with glassmorphism and smooth animations.
- **Smart Popups**: Complete car narratives with specifications in modal dialogs.

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

## How to Run

Since this is a static website, you can serve it using any simple HTTP server.

### Using Python

1. Navigate to the project directory:
   ```bash
   cd public
   ```

2. Start a local server:
   ```bash
   python3 -m http.server 8080
   ```

3. Open your browser and visit: `http://localhost:8080/home.html`

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

## Customization

### Adding a New Brand
1. Add car cards to `public/main.html` within a new `<h1>Brand Name</h1>` section.
2. Add descriptions in `scripts/enrich_data.py` DATA dictionary.
3. Run `python3 scripts/enrich_data.py`.
4. Run `python3 scripts/refactor.py`.

### Modifying Styles
Edit `public/style.css` to customize colors, layouts, and animations.

## Technologies

- **HTML5**
- **CSS3** (Glassmorphism, CSS Variables, Animations)
- **JavaScript** (Search, Modals, Interactivity)
- **Python** (Static Site Generation)

## Recent Updates

### January 2026
- **Fixed Page Layout**: Implemented a fixed header bar with glassmorphism to resolve overlapping issues.
- **Brand Color System**: Implemented authentic color schemes for all luxury brands.
- **UI Refinements**: Improved heading gradients, animation effects, and spacing.

Enjoy exploring the world's most amazing cars! 🚗✨
