# src/rbgen/backgrounds/textures.py
import random
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from rbgen.backgrounds.utils import (
    generate_perlin_noise,
)


def apply_perlin_noise_background(image, colors, scale=0.1, octaves=6):
    """
    Creates a Perlin noise background with smooth transitions between colors.
    Uses RegularGridInterpolator instead of deprecated interp2d.

    Args:
        image: PIL Image with transparency
        colors: Tuple of two RGB colors to interpolate between
        scale: Scale of the noise (smaller = more zoomed out)
        octaves: Number of detail levels in the noise

    Returns:
        PIL.Image: Image with applied Perlin noise background.
    """
    width, height = image.size
    background = Image.new("RGBA", (width, height))
    pixels = background.load()

    # Generate the noise
    noise = generate_perlin_noise(width, height, scale, octaves)

    # Convert to image with color interpolation
    for y in range(height):
        for x in range(width):
            t = noise[y, x]
            r = int(colors[0][0] * (1 - t) + colors[1][0] * t)
            g = int(colors[0][1] * (1 - t) + colors[1][1] * t)
            b = int(colors[0][2] * (1 - t) + colors[1][2] * t)
            pixels[x, y] = (r, g, b, 255)

    # Apply the original image with transparency
    background.paste(image, (0, 0), image)
    return background


def apply_gradient_background(image, colors, direction="horizontal"):
    """
    Creates a smooth gradient background.

    Args:
        image: PIL Image with transparency
        colors: Tuple of two RGB colors for gradient start and end
        direction: Direction of gradient
            ("horizontal", "vertical", "diagonal", "radial")

    Returns:
        PIL.Image: Image with applied gradient background.
    """
    width, height = image.size
    background = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(background)

    # Choose a random direction if not specified
    if direction == "random":
        direction = random.choice(["horizontal", "vertical", "diagonal", "radial"])

    if direction == "horizontal":
        for x in range(width):
            t = x / width
            r = int(colors[0][0] * (1 - t) + colors[1][0] * t)
            g = int(colors[0][1] * (1 - t) + colors[1][1] * t)
            b = int(colors[0][2] * (1 - t) + colors[1][2] * t)
            draw.line([(x, 0), (x, height)], fill=(r, g, b, 255))

    elif direction == "vertical":
        for y in range(height):
            t = y / height
            r = int(colors[0][0] * (1 - t) + colors[1][0] * t)
            g = int(colors[0][1] * (1 - t) + colors[1][1] * t)
            b = int(colors[0][2] * (1 - t) + colors[1][2] * t)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    elif direction == "diagonal":
        max_distance = math.sqrt(width**2 + height**2)
        for y in range(height):
            for x in range(width):
                # Calculate distance from top-left corner
                dist = math.sqrt(x**2 + y**2)
                t = dist / max_distance
                r = int(colors[0][0] * (1 - t) + colors[1][0] * t)
                g = int(colors[0][1] * (1 - t) + colors[1][1] * t)
                b = int(colors[0][2] * (1 - t) + colors[1][2] * t)
                draw.point((x, y), fill=(r, g, b, 255))

    elif direction == "radial":
        center_x, center_y = width // 2, height // 2
        max_radius = max(width, height) // 2

        for y in range(height):
            for x in range(width):
                distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                t = min(1.0, distance / max_radius)
                r = int(colors[0][0] * (1 - t) + colors[1][0] * t)
                g = int(colors[0][1] * (1 - t) + colors[1][1] * t)
                b = int(colors[0][2] * (1 - t) + colors[1][2] * t)
                draw.point((x, y), fill=(r, g, b, 255))

    background.paste(image, (0, 0), image)
    return background


def apply_radial_pattern_background(image, colors, num_rays=24):
    """
    Creates a radial pattern with rays emanating from the center.

    Args:
        image: PIL Image with transparency
        colors: Tuple of two RGB colors for alternating rays
        num_rays: Number of rays in the pattern
    """
    width, height = image.size
    background = Image.new("RGBA", (width, height), colors[0] + (255,))
    draw = ImageDraw.Draw(background)

    center_x, center_y = width // 2, height // 2
    ray_angle = 360 / num_rays
    max_radius = math.sqrt((width // 2) ** 2 + (height // 2) ** 2)

    for i in range(num_rays):
        if i % 2 == 1:  # Only draw every other ray (alternate colors)
            start_angle = i * ray_angle
            end_angle = (i + 1) * ray_angle

            # Draw a filled ray/segment
            draw.pieslice(
                (
                    center_x - max_radius,
                    center_y - max_radius,
                    center_x + max_radius,
                    center_y + max_radius,
                ),
                start_angle,
                end_angle,
                fill=colors[1] + (255,),
            )

    background.paste(image, (0, 0), image)
    return background


def apply_marble_texture_background(
    image, colors, turbulence=5.0, scale=0.05, octaves=5, vein_scale=25.0
):
    """
    Creates a realistic marble texture using Perlin noise with non-linear
    transformations.

    Args:
        image: PIL Image with transparency
        colors: List of RGB colors for marble veins (can be more than two)
        turbulence: Amount of turbulence in the marble pattern
        scale: Base scale for the noise (lower = larger features)
        octaves: Number of noise layers to combine
        vein_scale: Scale factor for vein width variation

    Returns:
        PIL.Image: Image with applied realistic marble texture background.
    """
    width, height = image.size

    # Expand canvas by 20%
    new_width = int(width * 1.2)
    new_height = int(height * 1.2)

    # Generate direction field for vein orientation
    direction_noise_x = generate_perlin_noise(new_width, new_height, scale / 3, 2)
    direction_noise_y = generate_perlin_noise(
        new_width, new_height, scale / 3, 2, seed=42
    )

    # Create direction vectors from noise
    direction_field = np.zeros((new_height, new_width, 2))
    for y in range(new_height):
        for x in range(new_width):
            angle = (direction_noise_x[y, x] + direction_noise_y[y, x]) * math.pi
            direction_field[y, x] = [math.cos(angle), math.sin(angle)]

    # Generate base Perlin noise textures
    base_noise = generate_perlin_noise(new_width, new_height, scale, octaves)
    vein_width_noise = generate_perlin_noise(new_width, new_height, scale * 2, 2)
    detail_noise = generate_perlin_noise(new_width, new_height, scale * 4, 3)

    # Create marble texture
    marble_texture = np.zeros((new_height, new_width))
    for y in range(new_height):
        for x in range(new_width):
            dx, dy = direction_field[y, x]
            distortion = turbulence * base_noise[y, x]
            sample_x = x + dx * distortion
            sample_y = y + dy * distortion
            wrapped_x = int(sample_x) % new_width
            wrapped_y = int(sample_y) % new_height
            vein_freq = 1.0 + vein_width_noise[y, x] * 0.5
            value = math.sin(
                ((x + y * 0.5) / vein_scale + base_noise[wrapped_y, wrapped_x] * 2)
                * vein_freq
            )
            marble_texture[y, x] = (value * 0.7 + 0.7 + detail_noise[y, x] * 0.3) * 0.5

    # Normalize contrast
    marble_texture = np.clip(marble_texture, 0, 1)

    # Create the background RGBA array
    result = np.zeros((new_height, new_width, 4), dtype=np.uint8)
    for y in range(new_height):
        for x in range(new_width):
            t = math.pow(marble_texture[y, x], 1.2)
            if len(colors) == 2:
                r = int(colors[0][0] * (1 - t) + colors[1][0] * t)
                g = int(colors[0][1] * (1 - t) + colors[1][1] * t)
                b = int(colors[0][2] * (1 - t) + colors[1][2] * t)
            else:
                idx = min(int(t * (len(colors) - 1) * 0.9999), len(colors) - 2)
                blend = (t * (len(colors) - 1)) - idx
                blend += (detail_noise[y, x] - 0.5) * 0.1
                blend = max(0, min(1, blend))
                c1 = colors[idx]
                c2 = colors[idx + 1]
                r = int(c1[0] * (1 - blend) + c2[0] * blend)
                g = int(c1[1] * (1 - blend) + c2[1] * blend)
                b = int(c1[2] * (1 - blend) + c2[2] * blend)
            result[y, x] = [r, g, b, 255]

    # Convert to PIL Image
    marble_image = Image.fromarray(result, "RGBA")

    # Apply subtle blur
    marble_image = marble_image.filter(ImageFilter.GaussianBlur(radius=1.2))

    # Add subtle surface variation and dithering
    surface_noise = generate_perlin_noise(new_width, new_height, scale * 8, 2)
    dither_noise = np.random.rand(new_height, new_width) * 3 - 1.5
    for y in range(new_height):
        for x in range(new_width):
            r, g, b, a = marble_image.getpixel((x, y))
            detail = int((surface_noise[y, x] - 0.5) * 6 + dither_noise[y, x])
            r = max(0, min(255, r + detail))
            g = max(0, min(255, g + detail))
            b = max(0, min(255, b + detail))
            marble_image.putpixel((x, y), (r, g, b, a))

    # Crop the bottom-right section to avoid heavy banding artifacts
    # Reduce vein_scale or expansion factor if desired.
    left = new_width - width
    top = new_height - height
    marble_image = marble_image.crop((left, top, left + width, top + height))

    # Blend with the original image
    marble_image.paste(image, (0, 0), image)

    return marble_image


def apply_cloud_background(image, colors, scale=0.5, octaves=4, seed=None):
    """
    Creates a light cloud-like texture using Perlin noise with multiple octaves.

    Args:
        image: PIL Image with transparency.
        colors: Tuple of two RGB colors for the cloud texture.
        scale: Base scale of the noise.
        octaves: Number of noise layers combined.
        seed: Random seed for noise generation (optional).

    Returns:
        PIL.Image: Image with an applied cloud-like texture background.
    """
    width, height = image.size
    background = Image.new("RGBA", (width, height))
    pixels = background.load()

    # Generate Perlin noise
    noise_map = generate_perlin_noise(width, height, scale, octaves, seed)

    for y in range(height):
        for x in range(width):
            # Apply cloud-like transform
            # t = noise_map[y, x] ** 1.5  # less contrast
            t = np.clip(noise_map[y, x] ** 2.2, 0, 1)  # more contrast

            # Interpolate between colors
            r = int(colors[0][0] * (1 - t) + colors[1][0] * t)
            g = int(colors[0][1] * (1 - t) + colors[1][1] * t)
            b = int(colors[0][2] * (1 - t) + colors[1][2] * t)

            pixels[x, y] = (r, g, b, 255)

    # Apply stronger blur for larger images
    blur_radius = 2.0 if max(width, height) > 512 else 1.5
    background = background.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # Paste original image with transparency
    background.paste(image, (0, 0), image)
    return background
