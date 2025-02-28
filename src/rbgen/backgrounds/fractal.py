# src/rbgen/backgrounds/fractal.py
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from rbgen.backgrounds.utils import interpolate_color, compose_images


def apply_mandelbrot_background(image, colors, max_iter=100, zoom=None, center=None):
    """
    Applies a Mandelbrot fractal background to an image with transparency.

    Args:
    image (PIL.Image): The image with transparency.
    colors (tuple): Tuple of two RGB color tuples for gradient mapping.
    max_iter (int, optional): Maximum iterations for the fractal calculation.
        Default is 100.
    zoom (float, optional): Zoom level for the fractal. If None, a random
        value is used.
    center (tuple, optional): Center coordinates (x, y) for the fractal.
        If None, random values are used.

    Returns:
        PIL.Image: Image with fractal background
    """
    width, height = image.size
    background = Image.new("RGBA", (width, height))
    pixels = background.load()

    # Use provided parameters or randomize if not specified
    zoom = zoom if zoom is not None else random.uniform(0.8, 3.5)

    if center is not None:
        center_x, center_y = center
    else:
        center_x = random.uniform(-1.0, 0.5)
        center_y = random.uniform(-0.5, 0.5)

    for y in range(height):
        for x in range(width):
            # Map pixel coordinates to complex plane
            zx = (x / width - 0.5) * (3.5 / zoom) + center_x
            zy = (y / height - 0.5) * (2.0 / zoom) + center_y

            # Initial values for iteration
            cx, cy = zx, zy

            # Mandelbrot iteration
            i = 0
            while zx * zx + zy * zy < 4 and i < max_iter:
                zx, zy = zx * zx - zy * zy + cx, 2.0 * zx * zy + cy
                i += 1

            # Color mapping based on iteration count
            t = i / max_iter
            pixels[x, y] = interpolate_color(colors[0], colors[1], t)

    # Composite the original image on top of the fractal background
    return compose_images(background, image)


def apply_nested_polygons_background(image, colors, line_width=3, depth=4):
    """
    Applies a fractal of recursive nested polygons using barycentric subdivision,
    with a random choice of gradient mapping techniques.

    Args:
        image (PIL.Image): The image with transparency.
        colors (tuple): A tuple of RGB color tuples used for gradient mapping.
        line_width (int, optional): Line width for polygon outlines.
            Default is 3
        depth (int, optional): Recursion depth for the fractal subdivision.
            Default is 4.

    Returns:
        PIL.Image: Image with fractal background.
    """
    width, height = image.size
    # Initialize as transparent background
    background = Image.new("RGBA", (width, height))
    # For black background use:
    # background = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    draw = ImageDraw.Draw(background)

    gradient_type = random.choice(["linear", "radial", "vertex"])
    stack = [(width // 2, height // 2, min(width, height) / 2, depth, None)]

    while stack:
        x, y, size, depth, sides = stack.pop()

        if depth == 0 or size < 1:
            continue

        sides = sides or random.randint(3, 8)
        angle = 2 * np.pi / sides
        vertices = [
            (
                x + size * np.cos(i * angle + random.uniform(-0.05, 0.05)),
                y + size * np.sin(i * angle + random.uniform(-0.05, 0.05)),
            )
            for i in range(sides)
        ]

        if gradient_type == "linear":
            color1, color2 = random.sample(colors, 2)
            poly_color = interpolate_color(color1, color2, random.uniform(0, 1))
        elif gradient_type == "radial":
            center_color = random.choice(colors)
            edge_color = random.choice(colors)
            distance_factor = min(size / width, size / height)
            poly_color = interpolate_color(center_color, edge_color, distance_factor)
        else:  # "vertex"
            poly_color = random.choice(colors)

        # Adjust line width as needed
        draw.polygon(vertices, outline=poly_color, width=line_width)

        # Subdivide
        new_size = size * random.uniform(0.45, 0.55)
        for vx, vy in vertices:
            stack.append(
                (
                    vx + random.uniform(-3, 3),
                    vy + random.uniform(-3, 3),
                    new_size,
                    depth - 1,
                    sides,
                )
            )

    background = background.filter(ImageFilter.GaussianBlur(0.5))

    return compose_images(background, image)
