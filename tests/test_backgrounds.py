# tests/test_backgrounds.py
import pytest
from pathlib import Path
from rbgen.color_schemes.color_utils import generate_color_pair

def test_get_available_background_modes(image_processor):
    """Test if all expected background modes are available."""
    expected_modes = {
        "solid", "striped", "checkered", "perspective_checkered",
        "mandelbrot", "nested_polygons", "geometric_shapes", 
        "concentric_shapes", "line", "wavy_line", "perlin_noise", 
        "gradient", "radial_pattern", "marble", "cloud", "waves"
    }
    
    modes = set(image_processor.get_available_background_modes())
    missing_modes = expected_modes - modes
    extra_modes = modes - expected_modes

    assert missing_modes == set(), f"Missing modes: {missing_modes}"
    assert extra_modes == set(), f"Unexpected modes: {extra_modes}"

@pytest.mark.parametrize("mode", [
    "solid", "striped", "checkered", "perspective_checkered",
    "mandelbrot", "nested_polygons", "geometric_shapes", 
    "concentric_shapes", "line", "wavy_line", "perlin_noise", 
    "gradient", "radial_pattern", "marble", "cloud", "waves"
])
def test_generate_backgrounds(mode, image_processor, sample_image, output_dir):
    """Test generating each type of background and saving the output."""
    output_path = Path(output_dir) / f"test_{mode}.png"
    
    # Generate a color pair for testing
    colors = generate_color_pair()

    # Generate the background
    result = image_processor.process_image(sample_image, mode=mode, colors=colors)
    
    # Ensure the output is a valid image
    assert result is not None, f"Background generation failed for mode: {mode}"
    assert result.size == sample_image.size, f"Size mismatch for mode: {mode}"

    # Save for debugging if needed
    result.save(output_path)
    
    # Check if the file was successfully created
    assert output_path.exists(), f"Output file was not created for mode: {mode}"

