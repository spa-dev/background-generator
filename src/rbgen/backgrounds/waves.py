# src/rbgen/backgrounds/waves.py
import random
import math
from PIL import Image, ImageDraw
from rbgen.backgrounds.utils import interpolate_color, compose_images


def apply_waves_background(
    image,
    colors,
    num_waves=10,
    wave_height_range=(10, 50),
    wave_types=None,
    direction="horizontal",
):
    """
    Generates a background with wave patterns.

    Args:
        image (PIL.Image): Base image to overlay the background.
        colors (list): List of two colors to interpolate.
        num_waves (int): Number of wave layers to generate.
        wave_height_range (tuple): Range for wave height (min, max).
        wave_types (list, optional): List of wave types to use.
            Defaults to ["sine", "triangle", "ripple"].
        direction (str): Direction of waves - "horizontal" or "vertical".

    Returns:
        PIL.Image: Image with wave background.
    """
    width, height = image.size

    # Increase background size by 15% to help avoid edge artifacts
    extra_margin_w = int(0.15 * width)
    extra_margin_h = int(0.15 * height)
    expanded_width = width + 2 * extra_margin_w
    expanded_height = height + 2 * extra_margin_h

    # Randomly pick background color
    base_color = random.choice(colors) + (255,)  # Ensure full opacity

    # Create a larger background filled with the base color
    background = Image.new("RGBA", (expanded_width, expanded_height), base_color)
    draw = ImageDraw.Draw(background)

    if wave_types is None:
        wave_types = ["sine", "triangle", "ripple"]

    # Determine if waves run horizontally or vertically
    is_horizontal = direction.lower() == "horizontal"
    span = expanded_width if is_horizontal else expanded_height
    thickness = expanded_height if is_horizontal else expanded_width

    # Create multiple wave layers
    for layer in range(num_waves):
        # Randomize wave parameters
        wave_type = random.choice(wave_types)
        wave_height = random.uniform(*wave_height_range)
        frequency = random.uniform(1, 5) / span  # Waves per pixel
        phase = random.uniform(0, 2 * math.pi)  # Random starting phase

        # Layer position - distribute evenly but with some randomness
        layer_position = thickness * (layer / num_waves) + (
            random.uniform(-thickness / num_waves / 4, thickness / num_waves / 4)
        )

        # Color based on layer position
        t = layer / (num_waves - 1) if num_waves > 1 else 0.5
        color = interpolate_color(colors[0], colors[1], t)

        # Define points for the wave
        points = []

        # Start with the bottom-left corner
        if is_horizontal:
            points.append((0, thickness))
        else:
            points.append((0, 0))

        # Generate wave points
        for i in range(0, span + 1, 2):
            if wave_type == "sine":
                amplitude = wave_height * math.sin(frequency * i * 2 * math.pi + phase)
            elif wave_type == "triangle":
                x = (frequency * i + phase / (2 * math.pi)) % 1
                amplitude = wave_height * (4 * abs(x - 0.5) - 1)
            elif wave_type == "ripple":
                center_dist = abs(i - span / 2) / (span / 2)
                local_height = wave_height * (1 - center_dist**2)
                amplitude = local_height * math.sin(frequency * i * 2 * math.pi + phase)

            # Add point to the wave
            if is_horizontal:
                points.append((i, layer_position + amplitude))
            else:
                points.append((layer_position + amplitude, i))

        # Close the polygon by adding corner points
        if is_horizontal:
            points.append((span, thickness))
        else:
            points.append((thickness, span))
            points.append((thickness, 0))

        # Draw the wave as a filled polygon
        draw.polygon(points, fill=color, outline=None)

    # Crop back to the original size
    cropped_background = background.crop(
        (
            extra_margin_w,
            extra_margin_h,
            extra_margin_w + width,
            extra_margin_h + height,
        )
    )

    return compose_images(cropped_background, image)
