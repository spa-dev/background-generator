# src/rbgen/backgrounds/utils.py
import numpy as np
from scipy.interpolate import RegularGridInterpolator


def find_perspective_coeffs(src, dst):
    """
    Calculate the coefficients for a perspective transformation.

    Args:
        src: Source quadrilateral coordinates
        dst: Destination quadrilateral coordinates

    Returns:
        list: Perspective transformation coefficients
    """
    matrix = []
    for p1, p2 in zip(dst, src):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])
    A = np.array(matrix, dtype=np.float32)
    B = np.array(src, dtype=np.float32).reshape(8)
    res = np.linalg.solve(A, B)
    return res.tolist()


def interpolate_color(c1, c2, t):
    """
    Blend two colors based on a factor t (0 to 1).

    Args:
        c1 (tuple): First RGB color tuple
        c2 (tuple): Second RGB color tuple
        t (float): Interpolation factor (0.0 to 1.0)

    Returns:
        tuple: Blended RGBA color
    """
    return tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3)) + (255,)


def compose_images(background, foreground):
    """
    Compose a foreground image with transparency onto a background image.

    Args:
        background (PIL.Image): Background image
        foreground (PIL.Image): Foreground image with transparency

    Returns:
        PIL.Image: Composed image
    """
    if background.size != foreground.size:
        background = background.resize(foreground.size)

    result = background.copy()
    result.paste(foreground, (0, 0), foreground)
    return result


def generate_perlin_noise(width, height, scale, octaves, seed=None):
    """
    Generate Perlin noise with a specified seed for reproducibility.
    Lacks an implementation of persistence and lacunarity.

    Args:
        width: Width of the output noise array
        height: Height of the output noise array
        scale: Base scale factor for the noise
        octaves: Number of noise layers to combine
        seed: Random seed for reproducibility.
            Default: None, which uses a random seed

    Returns:
        np.array: 2D array of Perlin noise values normalized to 0-1 range
    """
    MAX_GRID_SIZE = 2048  # Prevent extreme memory usage

    # Set the random seed if provided
    if seed is not None:
        np.random.seed(seed)

    noise = np.zeros((height, width), dtype=np.float32)
    # Parameters for different noise frequencies
    persistence = 0.5
    amplitude = 1.0
    frequency = scale
    max_value = 0

    # Generate multiple noise octaves and combine them
    for i in range(octaves):
        if i > 0:
            frequency *= 2
            amplitude *= persistence

        # Generate random grid
        grid_width = min(int(width * frequency) + 2, MAX_GRID_SIZE)
        grid_height = min(int(height * frequency) + 2, MAX_GRID_SIZE)

        # Random gradients grid
        grid = np.random.rand(grid_height, grid_width) * 2 - 1

        # Create interpolator
        y_coords = np.linspace(0, grid_height - 1, grid_height)
        x_coords = np.linspace(0, grid_width - 1, grid_width)
        interpolator = RegularGridInterpolator(
            (y_coords, x_coords),
            grid,
            method="linear",
            bounds_error=False,
            fill_value=None,
        )

        # Sample at pixel locations
        y_sample = np.linspace(0, grid_height - 1, height)
        x_sample = np.linspace(0, grid_width - 1, width)
        pts = np.array(np.meshgrid(y_sample, x_sample, indexing="ij")).T.reshape(-1, 2)
        noise_layer = interpolator(pts).reshape(height, width)

        # Add this octave to the total noise
        noise += noise_layer * amplitude
        max_value += amplitude

    # Reset the random seed if it was set
    if seed is not None:
        np.random.seed(None)

    # Normalize noise to 0-1 range
    noise = (noise + max_value) / (max_value * 2)
    return np.clip(noise, 0, 1)