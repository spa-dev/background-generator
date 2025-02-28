# src/rbgen/backgrounds/__init__.py
from rbgen.backgrounds.solid import apply_solid_background
from rbgen.backgrounds.striped import apply_striped_background
from rbgen.backgrounds.checkered import (
    apply_checkered_background, 
    apply_perspective_checkered_background,
)
from rbgen.backgrounds.fractal import (
    apply_mandelbrot_background,
    apply_nested_polygons_background
)
from rbgen.backgrounds.shapes import (
    apply_geometric_shapes_background,
    apply_concentric_shapes_background
)
from rbgen.backgrounds.line import (
    apply_line_background, 
    apply_wavy_line_background
)
from rbgen.backgrounds.textures import (
    apply_perlin_noise_background,
    apply_gradient_background,
    apply_radial_pattern_background,
    apply_marble_texture_background,
    apply_cloud_background
)
from rbgen.backgrounds.utils import (
    find_perspective_coeffs,
    interpolate_color,
    compose_images,
    generate_perlin_noise,
)

from rbgen.backgrounds.waves import (
    apply_waves_background,
)

__all__ = [
    # Solid and striped backgrounds
    "apply_solid_background",
    "apply_striped_background",
    # Checkered backgrounds
    "apply_checkered_background",
    "apply_perspective_checkered_background",
    # Fractal backgrounds
    "apply_mandelbrot_background",
    "apply_nested_polygons_background",
    # Shapes
    "apply_geometric_shapes_background",
    "apply_concentric_shapes_background",
    # Line-based background
    "apply_line_background",
    "apply_wavy_line_background",
    # Texture-based backgrounds
    "apply_perlin_noise_background",
    "apply_gradient_background",
    "apply_radial_pattern_background",
    "apply_marble_texture_background",
    "apply_cloud_background",
    # Utility functions
    "find_perspective_coeffs",
    "interpolate_color",
    #"create_gradient_background",
    "compose_images",
    #"add_noise",
    "generate_perlin_noise",
    # Waves
    "apply_waves_background",
]

