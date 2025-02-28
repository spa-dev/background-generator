# tests/conftest.py
import pytest
from pathlib import Path
from PIL import Image
from rbgen.processing.image_processor import ImageProcessor

@pytest.fixture
def output_dir():
    """Provide permanent directory for image outputs"""
    # Create a permanent directory in your tests folder
    output_path = Path(__file__).parent / "test_output"
    output_path.mkdir(exist_ok=True)
    return str(output_path)  # Convert to string 

#@pytest.fixture
#def output_dir(tmp_path):
#    """Provide temporary directory for image outputs"""
#    output_path = tmp_path / "render_output"
#    output_path.mkdir(exist_ok=True)
#    return str(output_path)  # Convert to string

@pytest.fixture
def image_processor():
    """Provide an instance of the ImageProcessor"""
    return ImageProcessor()

@pytest.fixture
def sample_image():
    """Generate a small sample transparent PNG image"""
    img = Image.new("RGBA", (500, 500), (255, 255, 255, 0))
    return img

