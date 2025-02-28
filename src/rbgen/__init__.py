# src/rbgen/__init__.py
"""
rbgen - random background generator
A package for applying various backgrounds and textures to transparent images.
"""
from rbgen.processing.image_processor import ImageProcessor
from rbgen.color_schemes.color_utils import (
    get_complementary,
    get_analogous,
    get_triadic,
    get_monochromatic,
    get_split_complementary,
    get_tetradic,
    generate_color_pair,
)
from rbgen.color_schemes.palettes import (
    BASE_COLOR_OPTIONS, 
    THEME_COLOR_SCHEMES, 
    get_themed_color_scheme,
)

# Import backgrounds as a module
from rbgen import backgrounds

__all__ = [
    "ImageProcessor",
    "get_complementary",
    "get_analogous",
    "get_triadic",
    "get_monochromatic",
    "get_split_complementary",
    "get_tetradic",
    "generate_color_pair",
    "BASE_COLOR_OPTIONS",
    "THEME_COLOR_SCHEMES",
    "get_themed_color_scheme",
    "backgrounds"
]


