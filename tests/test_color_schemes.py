# tests/test_color_schemes.py
import pytest
from pathlib import Path
from rbgen.color_schemes.palettes import THEME_COLOR_SCHEMES, get_themed_color_scheme
from rbgen.color_schemes.color_utils import generate_color_pair


@pytest.mark.parametrize("theme", list(THEME_COLOR_SCHEMES.keys()))
def test_generate_theme_color_backgrounds(
    theme, image_processor, sample_image, output_dir
):
    """Test generating backgrounds using all theme-based color schemes."""
    output_path = Path(output_dir) / f"test_{theme}.png"

    # Get a themed color scheme
    colors = get_themed_color_scheme(theme)

    # Generate the background using a default mode (e.g., "gradient")
    result = image_processor.process_image(sample_image, mode="gradient", colors=colors)

    # Ensure output is valid
    assert result is not None, f"Background generation failed for theme: {theme}"
    assert result.size == sample_image.size, f"Size mismatch for theme: {theme}"

    # Save for debugging
    result.save(output_path)

    # Check if file was successfully created
    assert output_path.exists(), f"Output file was not created for theme: {theme}"


def test_generate_color_pair():
    """Test generating a random color pair."""
    colors = generate_color_pair()

    assert isinstance(colors, list), "Output should be a list"
    assert len(colors) == 2, "Output should contain exactly two colors"
    assert all(
        isinstance(c, tuple) and len(c) == 3 for c in colors
    ), "Each color should be an RGB tuple (r, g, b)"
    assert all(
        0 <= value <= 255 for color in colors for value in color
    ), "RGB values should be in range 0-255"


def test_get_themed_color_scheme_valid():
    """Test that get_themed_color_scheme returns a valid color pair for known themes."""
    for theme in THEME_COLOR_SCHEMES.keys():
        color_pair = get_themed_color_scheme(theme)
        assert (
            color_pair in THEME_COLOR_SCHEMES[theme]
        ), f"Unexpected color pair {color_pair} for theme {theme}"


def test_get_themed_color_scheme_random():
    """Test that calling get_themed_color_scheme without a theme returns a valid color pair."""
    color_pair = get_themed_color_scheme()
    all_colors = [pair for pairs in THEME_COLOR_SCHEMES.values() for pair in pairs]
    assert color_pair in all_colors, f"Unexpected color pair {color_pair}"


def test_get_themed_color_scheme_invalid():
    """Test that an invalid theme raises a ValueError."""
    with pytest.raises(ValueError, match="Unknown theme: invalid_theme"):
        get_themed_color_scheme("invalid_theme")
