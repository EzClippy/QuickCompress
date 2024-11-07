import os
import sys
import hashlib
import pytest
from PIL import Image, ImageDraw
import pillow_avif  # Register AVIF plugin
from tkinter import Tk

# Adjust import path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.image_processing import resize_and_convert
from constants.constants import MAX_PIXELS_OPTIONS_DICT, SUPPORTED_IMAGE_FORMATS_IMPORT, SUPPORTED_IMAGE_FORMATS_EXPORT
from gui.image_converter_gui import ImageConverterGUI

@pytest.fixture
def generate_sample_images(tmp_path):
    """Generate sample images in various formats in the temporary directory."""
    width, height = 2048, 1080
    bar_height, bar_width = 100, 100
    image = Image.new('RGB', (width + 2 * bar_width, height + 2 * bar_height), 'white')
    draw = ImageDraw.Draw(image)

    draw.rectangle([0, 0, width + 2 * bar_width, bar_height], fill='black')
    draw.rectangle([0, height + bar_height, width + 2 * bar_width, height + 2 * bar_height], fill='gray')
    draw.rectangle([0, 0, bar_width, height + 2 * bar_height], fill='red')
    draw.rectangle([width + bar_width, 0, width + 2 * bar_width, height + 2 * bar_height], fill='blue')

    sample_images_dir = tmp_path / "sample_images"
    sample_images_dir.mkdir(exist_ok=True)

    formats = {
        'PNG': ['image.png'],
        'JPEG': ['image.jpeg', 'image.jpg'],
        'BMP': ['image.bmp'],
        'GIF': ['image.gif'],
        'WEBP': ['image.webp'],
        'AVIF': ['image.avif'],
        'TIFF': ['image.tiff', 'image.tif']
    }

    for fmt, filepaths in formats.items():
        for filepath in filepaths:
            image.save(sample_images_dir / filepath, format=fmt)
            print(f"Saved {filepath} in {fmt} format in {sample_images_dir}")

    return sample_images_dir

@pytest.fixture
def setup_app():
    root = Tk()
    app = ImageConverterGUI(root)
    yield app
    root.destroy()

def hash_filename(input_path, output_format, resolution_label):
    hasher = hashlib.sha256()
    hasher.update(input_path.encode())
    hasher.update(output_format.encode())
    hasher.update(resolution_label.encode())
    return hasher.hexdigest()

def normalize_format(format_str):
    return 'JPEG' if format_str.lower() in ('.jpg', '.jpeg') else format_str.lstrip('.').upper()

def test_image_conversion(generate_sample_images, tmp_path):
    sample_image_directory = generate_sample_images
    output_dir = tmp_path / "output_images"
    os.makedirs(output_dir, exist_ok=True)

    for input_format in SUPPORTED_IMAGE_FORMATS_IMPORT:
        input_image_path = os.path.join(sample_image_directory, f"image{input_format}")

        if not os.path.isfile(input_image_path):
            continue

        for export_format in SUPPORTED_IMAGE_FORMATS_EXPORT:
            for resolution_label, max_pixels in MAX_PIXELS_OPTIONS_DICT.items():
                hashed_filename = hash_filename(input_image_path, export_format, resolution_label)
                output_image_path = os.path.join(output_dir, f"{hashed_filename}{export_format}")

                success = resize_and_convert(
                    image_path=input_image_path,
                    output_path=output_image_path,
                    max_pixels=max_pixels,
                    compressed_format=export_format
                )

                assert success, f"Conversion failed for {input_image_path} to {export_format} at {resolution_label}"
                assert os.path.isfile(output_image_path), f"Output file not found: {output_image_path}"

                with Image.open(output_image_path) as img:
                    expected_format = normalize_format(export_format)
                    assert img.format == expected_format, f"Output format mismatch: {img.format} vs {expected_format}"
                    original_size = Image.open(input_image_path).size
                    if original_size[0] * original_size[1] > max_pixels:
                        assert img.size[0] * img.size[1] <= max_pixels, f"Output size exceeds max pixels for {resolution_label}"
                    print(f"Successfully converted {input_image_path} to {output_image_path} with resolution {resolution_label}")
