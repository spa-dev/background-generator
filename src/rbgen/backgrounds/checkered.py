# src/rbgen/backgrounds/checkered.py
import random
import math
from PIL import Image, ImageDraw
from rbgen.backgrounds.utils import find_perspective_coeffs, compose_images


def apply_checkered_background(image, colors, square_size=20):
    """
    Applies a randomly rotated checkered background to an image while keeping
    the foreground intact.

    Args:
        image (PIL.Image): The image with transparency.
        colors (tuple): A tuple of two RGB color tuples defining the
            colors in the checkered pattern.
        square_size (int, optional): The size of each checkered square.
            Defaults to 20.

    Returns:
        PIL.Image: The image with the applied checkered background.
    """
    width, height = image.size

    # Expand canvas to avoid cutoff during rotation
    diag = int(math.sqrt(width**2 + height**2))
    expanded_size = diag * 2  # Ensure coverage after rotation
    checkered = Image.new("RGBA", (expanded_size, expanded_size), colors[0] + (255,))
    draw = ImageDraw.Draw(checkered)

    # Draw checkered pattern on expanded canvas
    for x in range(0, expanded_size, square_size):
        for y in range(0, expanded_size, square_size):
            if (x // square_size + y // square_size) % 2 == 0:
                draw.rectangle(
                    [x, y, x + square_size, y + square_size], fill=colors[1] + (255,)
                )

    # Apply random rotation
    angle = random.uniform(0, 360)
    rotated = checkered.rotate(angle, resample=Image.BICUBIC, expand=True)

    # Crop center to match original size
    left = (rotated.width - width) // 2
    top = (rotated.height - height) // 2
    cropped = rotated.crop((left, top, left + width, top + height))

    return compose_images(cropped, image)


def apply_perspective_checkered_background(image, colors, square_size=40):
    """
    Applies a checkered background with shear, rotation, and perspective
    transformation to create a depth effect.

    Args:
        image (PIL.Image): The image with transparency.
        colors (tuple): A tuple of two RGB color tuples defining the
            checkered pattern.
        square_size (int, optional): The size of each checkered square.
            Defaults to 40.

    Returns:
        PIL.Image: The image with the transformed checkered background.
    """
    width, height = image.size

    # Expand canvas to ensure full coverage after transformations
    expand_factor = 2
    expanded_width = int(width * expand_factor)
    expanded_height = int(height * expand_factor)

    # Generate a checkered pattern
    background = Image.new(
        "RGBA", (expanded_width, expanded_height), colors[0] + (255,)
    )
    draw = ImageDraw.Draw(background)

    for x in range(0, expanded_width, square_size):
        for y in range(0, expanded_height, square_size):
            if (x // square_size + y // square_size) % 2 == 0:
                draw.rectangle(
                    [x, y, x + square_size, y + square_size], fill=colors[1] + (255,)
                )

    # Apply shear transformation manually
    # (since Image.transform doesn't support affine matrices directly)
    shear_x = random.uniform(-0.3, 0.3)
    shear_y = random.uniform(-0.1, 0.1)

    affine_matrix = (1, shear_x, 0, shear_y, 1, 0)  # (a, b, c, d, e, f)

    background = background.transform(
        (expanded_width, expanded_height),
        Image.AFFINE,
        affine_matrix,
        resample=Image.BILINEAR,
    )

    # Apply slight random rotation
    angle = random.uniform(-10, 10)
    background = background.rotate(angle, resample=Image.BILINEAR, expand=False)

    # Apply perspective transformation for depth effect
    vanish_x = expanded_width // 2  # Vanishing point in the center

    shrink_factor = 0.8  # Controls how much the tiles shrink into the distance

    # Perspective transform coefficients
    src_quad = [
        (0, 0),
        (expanded_width, 0),
        (expanded_width, expanded_height),
        (0, expanded_height),
    ]
    dst_quad = [
        (vanish_x - shrink_factor * expanded_width, 0),
        (vanish_x + shrink_factor * expanded_width, 0),
        (expanded_width, expanded_height),
        (0, expanded_height),
    ]

    coeffs = find_perspective_coeffs(src_quad, dst_quad)

    background = background.transform(
        (expanded_width, expanded_height),
        Image.PERSPECTIVE,
        coeffs,
        resample=Image.BILINEAR,
    )

    # Crop the final image to original dimensions
    left = (background.width - width) // 2
    top = (background.height - height) // 2
    background = background.crop((left, top, left + width, top + height))

    # Preserve the original image (foreground) with transparency
    return compose_images(background, image)
