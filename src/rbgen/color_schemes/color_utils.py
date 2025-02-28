# src/rbgen/color_schemes/color_utils.py
import random
import colorsys
import numpy as np
from rbgen.color_schemes.palettes import BASE_COLOR_OPTIONS


def get_complementary(base_color):
    """Generate a complementary color."""
    r, g, b = base_color
    return (255 - r, 255 - g, 255 - b)


def get_analogous(base_color, angle=30):
    """Generate an analogous color with given angle."""
    h, s, v = colorsys.rgb_to_hsv(
        base_color[0] / 255, base_color[1] / 255, base_color[2] / 255
    )
    h1 = (h + angle / 360) % 1
    rgb1 = colorsys.hsv_to_rgb(h1, s, v)
    return (int(rgb1[0] * 255), int(rgb1[1] * 255), int(rgb1[2] * 255))


def get_triadic(base_color):
    """Generate a triadic color."""
    h, s, v = colorsys.rgb_to_hsv(
        base_color[0] / 255, base_color[1] / 255, base_color[2] / 255
    )
    h1 = (h + 1 / 3) % 1
    rgb1 = colorsys.hsv_to_rgb(h1, s, v)
    return (int(rgb1[0] * 255), int(rgb1[1] * 255), int(rgb1[2] * 255))


def get_monochromatic(base_color, brightness_shift=0.2):
    """Generate a monochromatic variation."""
    h, s, v = colorsys.rgb_to_hsv(
        base_color[0] / 255, base_color[1] / 255, base_color[2] / 255
    )
    v_new = max(0, min(1, v + brightness_shift))
    rgb_new = colorsys.hsv_to_rgb(h, s, v_new)
    return (int(rgb_new[0] * 255), int(rgb_new[1] * 255), int(rgb_new[2] * 255))


def get_split_complementary(base_color):
    """Generate a split complementary color."""
    h, s, v = colorsys.rgb_to_hsv(
        base_color[0] / 255, base_color[1] / 255, base_color[2] / 255
    )
    h_comp = (h + 0.5) % 1
    h_split1 = (h_comp + 0.05) % 1
    rgb_split = colorsys.hsv_to_rgb(h_split1, s, v)
    return (int(rgb_split[0] * 255), int(rgb_split[1] * 255), int(rgb_split[2] * 255))


def get_tetradic(base_color):
    """Generate a tetradic color."""
    h, s, v = colorsys.rgb_to_hsv(
        base_color[0] / 255, base_color[1] / 255, base_color[2] / 255
    )
    h1 = (h + 0.25) % 1
    rgb1 = colorsys.hsv_to_rgb(h1, s, v)
    return (int(rgb1[0] * 255), int(rgb1[1] * 255), int(rgb1[2] * 255))


def generate_color_pair():
    """Generate a pair of colors using various color theory strategies.

    The function occasionally swaps the colors for variation.

    Returns:
        list: A list containing two RGB color tuples.
    """
    # Extract colors and weights
    base_colors, base_weights = zip(*BASE_COLOR_OPTIONS)

    # Choose color generation strategy
    color_strategy = random.choice(
        [
            "base_palette",   # Weight: 3
            "base_palette",
            "base_palette",
            "complementary",  # Weight: 2
            "complementary",
            "analogous",      # Weight: 2
            "analogous",
            "triadic",        # Weight: 1
            "monochromatic",  # Weight: 2
            "monochromatic",
            "split_comp",     # Weight: 1
            "tetradic",       # Weight: 1
        ]
    )

    if color_strategy == "base_palette":
        # Sample two different colors from the base palette
        while True:
            colors = random.sample(
                random.choices(base_colors, weights=base_weights, k=10), 2
            )
            if colors[0] != colors[1]:  # Avoid duplicate color pairs
                break
    else:
        # Use color theory to generate pairs
        base_color = random.choices(base_colors, weights=base_weights, k=1)[0]

        if color_strategy == "complementary":
            colors = [base_color, get_complementary(base_color)]
        elif color_strategy == "analogous":
            colors = [base_color, get_analogous(base_color)]
        elif color_strategy == "triadic":
            colors = [base_color, get_triadic(base_color)]
        elif color_strategy == "monochromatic":
            # Randomly choose brighter or darker
            shift = random.choice([0.2, -0.2])
            colors = [base_color, get_monochromatic(base_color, shift)]
        elif color_strategy == "split_comp":
            colors = [base_color, get_split_complementary(base_color)]
        elif color_strategy == "tetradic":
            colors = [base_color, get_tetradic(base_color)]

        # Occasionally swap the order
        if random.random() < 0.5:
            colors = colors[::-1]

    return colors
