# Luxury Car Gallery

A beautiful, interactive showcase website displaying luxury car collections from the world's most prestigious brands.

## Overview

This repository contains the generated static website for the Luxury Car Gallery. The project features a modern, responsive design with glassmorphism effects, smooth animations, and dedicated pages for various luxury car brands.

## Project Structure

```
repo/
├── public/               # The static website files
│   ├── home.html        # Main entry point (Homepage)
│   ├── *.html           # Individual brand pages
│   └── style.css        # Stylesheet
├── data/                 # Data files
│   └── descriptions.json        # Car descriptions and specs
└── car_list.txt         # Inventory list
```

## Features

- **Interactive Car Cards**: Detailed views with specifications and descriptions.
- **Brand-Specific Pages**: Dedicated pages for brands like BMW, Ferrari, Lamborghini, etc.
- **Authentic Brand Colors**: Each brand page features its specific brand identity colors.
  - BMW: Blue
  - Ferrari: Rosso Corsa
  - Lamborghini: Verde Mantis
  - And more...
- **Live Search**: Functionality to search across models.
- **Responsive Design**: Optimized for various screen sizes with a premium feel.

## How to Run

Since this is a static website, you can serve it using any simple HTTP server.

### Using Python

1. Navigate to the `public` directory:
   ```bash
   cd public
   ```

2. Start a local server:
   ```bash
   python3 -m http.server 8080
   ```

3. Open your browser and visit:
   `http://localhost:8080/home.html`

### Using VS Code Live Server

If you are using Visual Studio Code:
1. Open the `public/home.html` file.
2. Click "Go Live" (if you have the Live Server extension installed).

## Technologies

- **HTML5**
- **CSS3** (Glassmorphism, CSS Variables, Animations)
- **JavaScript** (Search, Modals, Interactivity)

## Recent Updates (January 2026)

- **Brand Color System**: Implemented authentic color schemes for all luxury brands.
- **UI Refinements**: Improved heading gradients and animation effects.

Enjoy exploring the world's most amazing cars! 🚗✨
