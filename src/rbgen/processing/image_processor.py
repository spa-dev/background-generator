# src/rbgen/processing/image_processor.py
import os
import random
from PIL import Image


class ImageProcessor:
    """
    Main class responsible for processing images with various background effects.
    """

    def __init__(self):
        """Initialize the processor with available background functions."""
        # These will be imported from their respective modules
        self.background_functions = {}
        self._register_background_functions()

    def _register_background_functions(self):
        """Register all available background functions from the backgrounds package."""
        # This will be populated from background modules
        from rbgen.backgrounds.solid import apply_solid_background
        from rbgen.backgrounds.striped import apply_striped_background
        from rbgen.backgrounds.checkered import (
            apply_checkered_background,
            apply_perspective_checkered_background,
        )
        from rbgen.backgrounds.fractal import (
            apply_mandelbrot_background,
            apply_nested_polygons_background,
        )
        from rbgen.backgrounds.shapes import (
            apply_geometric_shapes_background,
            apply_concentric_shapes_background,
        )
        from rbgen.backgrounds.line import (
            apply_line_background,
            apply_wavy_line_background,
        )
        from rbgen.backgrounds.textures import (
            apply_perlin_noise_background,
            apply_gradient_background,
            apply_radial_pattern_background,
            apply_marble_texture_background,
            apply_cloud_background,
        )
        from rbgen.backgrounds.waves import apply_waves_background

        # Register all functions with their keys
        self.background_functions = {
            "solid": apply_solid_background,
            "striped": apply_striped_background,
            "checkered": apply_checkered_background,
            "perspective_checkered": apply_perspective_checkered_background,
            "mandelbrot": apply_mandelbrot_background,
            "nested_polygons": apply_nested_polygons_background,
            "geometric_shapes": apply_geometric_shapes_background,
            "concentric_shapes": apply_concentric_shapes_background,
            "line": apply_line_background,
            "wavy_line": apply_wavy_line_background,
            "perlin_noise": apply_perlin_noise_background,
            "gradient": apply_gradient_background,
            "radial_pattern": apply_radial_pattern_background,
            "marble": apply_marble_texture_background,
            "cloud": apply_cloud_background,
            "waves": apply_waves_background,
        }

    def get_available_background_modes(self):
        """Return a list of all available background modes."""
        return list(self.background_functions.keys())

    def process_image(self, image, mode, colors, **kwargs):
        """
        Process a single image with the specified background mode and colors.

        Args:
            image: PIL Image object to process
            mode: Background mode to apply
            colors: List of colors to use
            **kwargs: Additional parameters for specific background modes

        Returns:
            Processed PIL Image
        """
        if mode not in self.background_functions:
            raise ValueError(f"Unknown background mode: {mode}")

        # Handle special cases with specific parameters
        # TODO: fix inconsistent handling of kwargs
        if mode == "solid":
            return self.background_functions[mode](image, colors[0])
        elif mode == "gradient" and "direction" in kwargs:
            return self.background_functions[mode](image, colors, kwargs["direction"])
        elif mode == "radial_pattern" and "num_rays" in kwargs:
            return self.background_functions[mode](image, colors, kwargs["num_rays"])
        elif mode == "perlin_noise" and "scale" in kwargs:
            return self.background_functions[mode](
                image, colors, kwargs.get("scale", 0.1), kwargs.get("octaves", 6)
            )
        elif mode == "marble" and "turbulence" in kwargs:
            return self.background_functions[mode](image, colors, kwargs["turbulence"])
        elif mode == "cloud":
            return self.background_functions[mode](
                image, colors, kwargs.get("scale", 0.5), kwargs.get("octaves", 4)
            )
        elif mode == "mandelbrot":
            return self.background_functions[mode](
                image,
                colors,
                kwargs.get("max_iter", 100),
                kwargs.get("zoom", None),
                kwargs.get("center", None),
            )
        elif mode == "nested_polygons":
            return self.background_functions[mode](
                image, colors, kwargs.get("line_width", 3), kwargs.get("depth", 4)
            )
        else:
            # Default case: Pass kwargs dynamically
            return self.background_functions[mode](image, colors, **kwargs)

    def process_directory(
        self, input_folder, output_folder, mode=None, colors=None, randomize=True
    ):
        """
        Process all PNG images in a directory, applying backgrounds.

        Args:
            input_folder: Path to folder containing input images
            output_folder: Path to save processed images
            mode: Background mode to apply (or None for random)
            colors: Colors to use (or None for random)
            randomize: Whether to randomize modes and colors
        """
        from rbgen.color_schemes.color_utils import generate_color_pair

        os.makedirs(output_folder, exist_ok=True)

        for filename in os.listdir(input_folder):
            if filename.lower().endswith(".png"):
                image_path = os.path.join(input_folder, filename)
                image = Image.open(image_path).convert("RGBA")

                if randomize:
                    # Get random mode
                    selected_mode = random.choice(
                        list(self.background_functions.keys())
                    )
                    # Get random color pair
                    selected_colors = generate_color_pair()

                    # Prepare additional parameters for specific modes
                    kwargs = {}
                    if selected_mode == "gradient":
                        kwargs["direction"] = random.choice(
                            ["horizontal", "vertical", "diagonal", "radial"]
                        )
                    elif selected_mode == "radial_pattern":
                        kwargs["num_rays"] = random.randint(4, 32)
                    elif selected_mode == "perlin_noise":
                        kwargs["scale"] = random.uniform(0.05, 0.3)
                        kwargs["octaves"] = random.randint(3, 8)
                    elif selected_mode == "marble":
                        kwargs["turbulence"] = random.uniform(3.0, 8.0)
                    elif selected_mode == "cloud":
                        kwargs["scale"] = random.uniform(10.0, 30.0)
                        kwargs["octaves"] = random.randint(3, 6)
                else:
                    selected_mode = mode
                    # Do `selected_colors = colors` to re-use the same colors
                    # Or to use random colors every image:
                    selected_colors = generate_color_pair()
                    
                    kwargs = {} # For non-random mode, kwargs passed separately

                # Process the image
                processed_image = self.process_image(
                    image, selected_mode, selected_colors, **kwargs
                )

                # Save the processed image
                output_path = os.path.join(output_folder, filename)
                processed_image.save(output_path)

                print(f"Processed: {filename} with {selected_mode} background")
