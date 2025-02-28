# src/rbgen/backgrounds/shapes.py
import random
import math
from PIL import Image, ImageDraw
from rbgen.backgrounds.utils import interpolate_color, compose_images


def apply_geometric_shapes_background(
    image, colors, num_shapes=50, max_size=100, shape_types=None
):
    """
    Generates a background with random overlapping geometric shapes.

    Args:
        image (PIL.Image): Base image to overlay the background.
        colors (list): List of two colors to interpolate.
        num_shapes (int): Number of shapes to generate.
        max_size (int): Maximum size of each shape.
        shape_types (list, optional): List of shape types to use.
                                     Defaults to ["circle", "triangle", "polygon"].

    Returns:
        PIL.Image: Image with geometric shapes background.
    """
    width, height = image.size
    background = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    draw = ImageDraw.Draw(background)

    if shape_types is None:
        shape_types = ["circle", "triangle", "polygon"]

    for _ in range(num_shapes):
        shape_type = random.choice(shape_types)
        x, y = random.randint(0, width), random.randint(0, height)
        size = random.randint(20, max_size)
        t = random.random()
        color = interpolate_color(colors[0], colors[1], t)

        if shape_type == "circle":
            draw.ellipse(
                [x - size, y - size, x + size, y + size], fill=color, outline=None
            )
        elif shape_type == "rectangle":
            draw.rectangle(
                [x - size, y - size, x + size, y + size], fill=color, outline=None
            )
        elif shape_type == "triangle":
            angle = random.uniform(0, 2 * math.pi)
            p1 = (x + size * math.cos(angle), y + size * math.sin(angle))
            p2 = (
                x + size * math.cos(angle + 2 * math.pi / 3),
                y + size * math.sin(angle + 2 * math.pi / 3),
            )
            p3 = (
                x + size * math.cos(angle + 4 * math.pi / 3),
                y + size * math.sin(angle + 4 * math.pi / 3),
            )
            draw.polygon([p1, p2, p3], fill=color, outline=None)
        elif shape_type == "polygon":
            num_sides = random.randint(4, 8)
            points = [
                (
                    x + size * math.cos(2 * math.pi * i / num_sides),
                    y + size * math.sin(2 * math.pi * i / num_sides),
                )
                for i in range(num_sides)
            ]
            draw.polygon(points, fill=color, outline=None)

    return compose_images(background, image)


def apply_concentric_shapes_background(
    image, colors, num_rings=10, center=None, shape_type=None
):
    """
    Generates a background with concentric shapes radiating from a center point.

    Args:
        image (PIL.Image): Base image to overlay the background.
        colors (list): List of two colors to interpolate.
        num_rings (int): Number of concentric shapes to draw.
        center (tuple, optional): Center position (x, y). If None, uses image center.
        shape_type (str): Type of shape to use ("circle", "square").

    Returns:
        PIL.Image: Image with concentric shapes background.
    """
    width, height = image.size
    background = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    draw = ImageDraw.Draw(background)

    if shape_type is None:
        shape_types = ["circle", "square"]
        shape_type = random.choice(shape_types)

    if center is None:
        center = (width // 2, height // 2)

    max_radius = max(width, height) * 0.75

    for i in range(num_rings, 0, -1):
        radius = (i / num_rings) * max_radius
        t = i / num_rings
        color = interpolate_color(colors[0], colors[1], t)

        if shape_type == "circle":
            draw.ellipse(
                [
                    center[0] - radius,
                    center[1] - radius,
                    center[0] + radius,
                    center[1] + radius,
                ],
                fill=color,
                outline=None,
            )
        elif shape_type == "square":
            draw.rectangle(
                [
                    center[0] - radius,
                    center[1] - radius,
                    center[0] + radius,
                    center[1] + radius,
                ],
                fill=color,
                outline=None,
            )

    return compose_images(background, image)
