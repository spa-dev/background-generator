# src/rbgen/backgrounds/striped.py
import math
import random
from PIL import Image, ImageDraw


def apply_striped_background(image, colors, min_stripe_width=10, max_stripe_width=30):
    """
    Applies a randomly rotated striped background with variable stripe widths
    while keeping the foreground intact.

    Parameters:
        image (PIL.Image): The foreground image with transparency.
        colors (tuple): A tuple of two RGB color tuples, (background_color, stripe_color).
        min_stripe_width (int, optional): Minimum width of stripes.
        max_stripe_width (int, optional): Maximum width of stripes.

    Returns:
        PIL.Image: The image with applied striped background.
    """
    width, height = image.size

    # Expand canvas to avoid cutoff during rotation
    diag = int(math.sqrt(width**2 + height**2))
    expanded_size = diag * 2
    striped = Image.new("RGBA", (expanded_size, expanded_size), colors[0] + (255,))
    draw = ImageDraw.Draw(striped)

    # Draw vertical stripes with random widths
    x = 0
    while x < expanded_size:
        stripe_width = random.randint(min_stripe_width, max_stripe_width)
        draw.rectangle([x, 0, x + stripe_width, expanded_size], fill=colors[1] + (255,))
        x += stripe_width * 2  # Maintain spacing

    # Random rotation
    angle = random.uniform(0, 360)
    rotated = striped.rotate(angle, resample=Image.BICUBIC, expand=True)

    # Crop center to match original size
    left = (rotated.width - width) // 2
    top = (rotated.height - height) // 2
    cropped = rotated.crop((left, top, left + width, top + height))

    # Composite with the original image
    cropped.paste(image, (0, 0), image)

    return cropped
