# src/rbgen/color_schemes/palettes.py
import random

# Define base colors with assigned weights
BASE_COLOR_OPTIONS = [
    # Earthy tones
    ((150, 75, 50), 2),       # Warm brown
    ((100, 150, 100), 2),     # Forest green
    ((180, 160, 140), 2),     # Light earth tone
    ((200, 180, 140), 2),     # Sandy beige
    ((160, 140, 120), 2),     # Soft taupe
    
    # Neutrals
    ((140, 140, 140), 2),     # Neutral gray
    ((90, 110, 120), 2),      # Slate gray
    ((255, 255, 255), 3),     # Pure white
    ((240, 240, 235), 3),     # Warm white
    ((220, 220, 220), 3),     # Soft light gray
    ((200, 200, 200), 3),     # Gentle medium gray
    ((180, 180, 180), 3),     # Neutral stone gray
    
    # Soft pastels
    ((170, 140, 190), 2),     # Muted lavender
    ((190, 170, 200), 2),     # Misty mauve
    ((220, 200, 180), 2),     # Warm off-white
    ((120, 160, 180), 2),     # Subtle ocean blue
    ((180, 100, 80), 2),      # Muted coral
    
    # Magical colors
    ((110, 90, 160), 1),      # Twilight purple
    ((60, 100, 150), 1),      # Deep blue
    ((180, 140, 100), 1),     # Golden dusk
    ((200, 110, 80), 1),      # Sunset orange
    
    # Vibrant accents
    ((240, 180, 100), 1),     # Golden amber
    ((210, 100, 120), 1),     # Vintage rose pink
    ((70, 180, 190), 1),      # Teal
    ((230, 130, 60), 1),      # Burnt orange
    ((80, 170, 90), 1),       # Spring green
    
    # Pure/Strong colors
    ((255, 0, 0), 1),         # Red
    ((0, 255, 0), 1),         # Green
    ((0, 0, 255), 1),         # Blue
    ((255, 255, 0), 1),       # Yellow
    ((255, 0, 255), 1),       # Magenta
    ((0, 255, 255), 1),       # Cyan
    
    # Rich colors
    ((90, 40, 80), 1),        # Deep plum
    ((35, 55, 75), 1),        # Midnight navy
    ((200, 160, 60), 1),      # Old gold
    ((140, 30, 40), 1),       # Burgundy
    ((30, 70, 45), 1),        # Deep forest
    ((150, 95, 30), 1),       # Copper brown
    ((220, 190, 220), 1),     # Lilac
    ((190, 210, 200), 1),     # Mint sage
]

# Predefined color schemes for specific moods/themes
THEME_COLOR_SCHEMES = {
    "forest": [
        ((30, 70, 45), (80, 120, 90)),      # Deep forest + Moss
        ((60, 90, 60), (120, 150, 100)),    # Forest green + Light forest
        ((30, 60, 40), (100, 80, 60)),      # Dark pine + Brown bark
    ],
    
    "ocean": [
        ((40, 80, 120), (120, 180, 210)),   # Deep blue + Sky blue
        ((70, 140, 190), (200, 230, 240)),  # Ocean blue + Seafoam
        ((30, 60, 90), (70, 180, 190)),     # Navy + Teal
    ],
    
    "desert": [
        ((200, 180, 140), (230, 130, 60)),  # Sandy beige + Burnt orange
        ((180, 160, 120), (240, 180, 100)), # Dune + Golden amber
        ((160, 120, 80), (220, 200, 180)),  # Tan + Warm off-white
    ],
    
    "twilight": [
        ((70, 40, 90), (180, 140, 200)),    # Deep purple + Lavender
        ((40, 40, 80), (110, 90, 160)),     # Night blue + Twilight purple
        ((60, 30, 70), (200, 110, 80)),     # Dark purple + Sunset orange
    ],
    
    "autumn": [
        ((150, 75, 50), (230, 130, 60)),    # Warm brown + Burnt orange
        ((180, 100, 60), (240, 180, 100)),  # Rust + Golden amber
        ((120, 60, 40), (200, 160, 60)),    # Auburn + Old gold
    ]
}

def get_themed_color_scheme(theme=None):
    """Get a color scheme from a specific theme, or random if none specified."""
    if theme is None:
        theme = random.choice(list(THEME_COLOR_SCHEMES.keys()))
        
    if theme not in THEME_COLOR_SCHEMES:
        raise ValueError(f"Unknown theme: {theme}")
        
    # Return a random color pair from the selected theme
    return random.choice(THEME_COLOR_SCHEMES[theme])
