# src/rbgen/backgrounds/line.py
import math
import random
from PIL import Image, ImageDraw, ImageFilter


def apply_line_background(image, colors):
    """Creates a smooth anti-aliased line background with three sets of lines.
    The three sets of lines are spaced approximately 120 degrees apart, to
    cover the image.
    """
    width, height = image.size
    alpha = image.getchannel("A")

    # Supersample for smoother lines (2x resolution)
    scale_factor = 2
    high_res_width = width * scale_factor
    high_res_height = height * scale_factor
    high_res = Image.new("RGBA", (high_res_width, high_res_height), colors[0] + (255,))
    draw = ImageDraw.Draw(high_res)

    # Generate three vanishing points, spaced out across the image
    def get_vanishing_point():
        edge = random.choice(["left", "right", "top", "bottom"])
        if edge == "left":
            return (
                random.randint(0, (width // 3) * scale_factor),
                random.randint(0, high_res_height),
            )
        elif edge == "right":
            return (
                random.randint((2 * width // 3) * scale_factor, high_res_width),
                random.randint(0, high_res_height),
            )
        elif edge == "top":
            return (
                random.randint(0, high_res_width),
                random.randint(0, (height // 3) * scale_factor),
            )
        else:  # bottom
            return (
                random.randint(0, high_res_width),
                random.randint((2 * height // 3) * scale_factor, high_res_height),
            )

    vanishing_points = [get_vanishing_point() for _ in range(3)]

    # Draw three sets of lines
    for vanish_x, vanish_y in vanishing_points:
        num_lines = random.randint(15, 25)
        for _ in range(num_lines):
            # Choose a random edge to start from
            edge = random.choice(["left", "right", "top", "bottom"])
            if edge in ["left", "right"]:
                start_x = 0 if edge == "left" else high_res_width
                start_y = random.randint(0, high_res_height)
            else:
                start_x = random.randint(0, high_res_width)
                start_y = 0 if edge == "top" else high_res_height

            # Draw line from edge to vanishing point
            draw.line(
                [(start_x, start_y), (vanish_x, vanish_y)],
                fill=colors[1] + (255,),
                width=random.randint(2, 5),
            )

    # Downscale to original size for anti-aliasing
    background = high_res.resize((width, height), Image.LANCZOS)

    # Apply slight blur for additional smoothing
    background = background.filter(ImageFilter.SMOOTH_MORE)

    # Restore the original foreground using the alpha channel
    final_image = Image.composite(image, background, alpha)

    return final_image


def apply_wavy_line_background(image, colors):
    """Creates a wave pattern where waves move in a random direction."""
    width, height = image.size
    alpha = image.getchannel("A")

    # Supersample for smoother waves (2x resolution)
    scale_factor = 2
    high_res_width = width * scale_factor
    high_res_height = height * scale_factor
    high_res = Image.new("RGBA", (high_res_width, high_res_height), colors[0] + (255,))
    draw = ImageDraw.Draw(high_res)

    wave_count = random.randint(10, 20)
    amplitude = random.randint(10, height // 5) * scale_factor
    frequency = random.uniform(0.005, 0.05) / scale_factor

    phase_shift = random.uniform(0, 2 * math.pi)
    angle = random.uniform(0, 2 * math.pi)  # Random angle in radians

    # Generate wave paths
    for _ in range(wave_count):
        start_x = random.randint(0, high_res_width)
        start_y = random.randint(0, high_res_height)

        points = []
        for i in range(-high_res_width, high_res_width, 2 * scale_factor):
            offset = amplitude * math.sin(frequency * i + phase_shift)
            x = start_x + i * math.cos(angle) + offset * math.sin(angle)
            y = start_y + i * math.sin(angle) - offset * math.cos(angle)
            points.append((x, y))

        # Random width between 2 to 5 pixels (scaled)
        line_width = random.randint(2, 5) * scale_factor
        draw.line(points, fill=colors[1] + (200,), width=line_width)

    # Downscale to original size for anti-aliasing
    background = high_res.resize((width, height), Image.LANCZOS)

    # Apply slight blur for additional smoothing
    background = background.filter(ImageFilter.SMOOTH_MORE)

    # Restore the original foreground using the alpha channel
    final_image = Image.composite(image, background, alpha)

    return final_image
