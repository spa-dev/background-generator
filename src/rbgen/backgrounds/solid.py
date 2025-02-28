# src/rbgen/backgrounds/solid.py
from PIL import Image


def apply_solid_background(image, color):
    """
    Applies a solid color background to an image with transparency.

    Args:
        image (PIL.Image): The image with transparency
        color (tuple): RGB color tuple (r, g, b)

    Returns:
        PIL.Image: Image with solid background
    """
    background = Image.new("RGBA", image.size, color + (255,))
    background.paste(image, (0, 0), image)
    return background
