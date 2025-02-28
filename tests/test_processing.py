# tests/test_processing.py

from pathlib import Path
from PIL import Image


def test_process_directory(image_processor, tmp_path, output_dir):
    """Test processing a directory of images."""
    input_dir = tmp_path / "input_images"
    input_dir.mkdir()

    # Create a sample image file
    img_path = input_dir / "test_image.png"
    img = Image.new("RGBA", (100, 100), (255, 255, 255, 0))  # Transparent image
    img.save(img_path)

    # Ensure output_dir is a valid Path
    output_dir = Path(output_dir)

    # Process the directory
    image_processor.process_directory(
        str(input_dir),
        str(output_dir),
        mode="solid",
        colors=[(255, 0, 0)],
        randomize=False,
    )

    processed_image_path = output_dir / "test_image.png"

    # Assertions
    assert (
        processed_image_path.exists()
    ), f"Processed image not found at {processed_image_path}"
    assert processed_image_path.is_file(), "Processed image path is not a file"
