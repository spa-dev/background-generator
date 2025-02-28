# src/rbgen/main.py
import argparse
from rbgen.processing.image_processor import ImageProcessor
from rbgen.color_schemes.color_utils import generate_color_pair
from rbgen.color_schemes.palettes import get_themed_color_scheme


def main():
    """Main entry point for the rbgen application."""
    parser = argparse.ArgumentParser(description="rbgen - random background generator")

    parser.add_argument("-i", "--input", help="Input directory with transparent images")
    parser.add_argument("-o", "--output", help="Output directory for processed images")
    parser.add_argument("-m", "--mode", help="Background mode to use (omit for random)")
    parser.add_argument("-t", "--theme", help="Color theme to use (omit for random)")
    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        default=False,
        help="Use random background mode and colors for each image",
    )
    parser.add_argument(
        "--list-modes", action="store_true", help="List all available background modes"
    )
    parser.add_argument(
        "--list-themes", action="store_true", help="List all available color themes"
    )

    args = parser.parse_args()

    # Handle listing modes and themes before checking required args
    if args.list_modes:
        processor = ImageProcessor()
        print("Available background modes:")
        for mode in processor.get_available_background_modes():
            print(f"  - {mode}")
        return

    if args.list_themes:
        from rbgen.color_schemes.palettes import THEME_COLOR_SCHEMES

        print("Available color themes:")
        for theme in THEME_COLOR_SCHEMES.keys():
            print(f"  - {theme}")
        return

    # Require input and output directories only if not listing
    if not args.input or not args.output:
        print(
            "Error: -i/--input and -o/--output are required unless listing themes or modes."
        )
        return

    # Initialize processor and process images
    processor = ImageProcessor()

    # Generate colors based on theme if provided
    colors = None
    if args.theme:
        try:
            colors = get_themed_color_scheme(args.theme)
        except ValueError as e:
            print(str(e))
            return
    elif not args.random:
        colors = generate_color_pair()

    processor.process_directory(
        args.input, args.output, mode=args.mode, colors=colors, randomize=args.random
    )

    print(f"Processing complete. Images saved to '{args.output}'")


if __name__ == "__main__":
    main()
