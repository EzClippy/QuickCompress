import os
from PIL import Image, ExifTags
from constants.constants import SUPPORTED_IMAGE_FORMATS_IMPORT

def resize_and_convert(image_path, output_path, max_pixels, compressed_format):
    try:
        with Image.open(image_path) as img:
            # Correct orientation based on EXIF data
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = img._getexif()
                if exif is not None:
                    orientation = exif.get(orientation)
                    if orientation == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation == 6:
                        img = img.rotate(270, expand=True)
                    elif orientation == 8:
                        img = img.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                # No EXIF data or orientation tag not found
                pass

            original_width, original_height = img.size
            original_area = original_width * original_height

            if original_area > max_pixels:
                scaling_factor = (max_pixels / original_area) ** 0.5
                new_width = int(original_width * scaling_factor)
                new_height = int(original_height * scaling_factor)
                resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            else:
                resized_img = img

            format_to_save = compressed_format.lstrip('.').upper()
            if format_to_save == 'JPG':
                format_to_save = 'JPEG'

            # Convert to RGB if saving as JPEG
            if format_to_save == 'JPEG' and resized_img.mode in ('P', 'RGBA', 'LA'):
                resized_img = resized_img.convert('RGB')

            output_path = os.path.splitext(output_path)[0] + compressed_format
            resized_img.save(output_path, format_to_save)
            print(f"Image successfully converted and saved to {output_path}.")
        return True
    except Exception as e:
        print(f"Error converting {image_path}: {e}")
        return False

def process_images_in_directory(input_directory, output_directory, progress_window, gui_instance, max_pixels, compressed_format):
    success = True
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    file_list = []
    for root, _, files in os.walk(input_directory):
        for file in files:
            if any(file.lower().endswith(ext) for exts in SUPPORTED_IMAGE_FORMATS_IMPORT.values() for ext in exts):
                file_list.append(os.path.join(root, file))

    total_files = len(file_list)

    for index, file_path in enumerate(file_list, start=1):
        if gui_instance.cancelled:
            success = False
            break

        output_path = os.path.join(output_directory, os.path.relpath(file_path, input_directory))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        file_success = resize_and_convert(file_path, output_path, max_pixels, compressed_format)
        if not file_success:
            success = False

        progress_value = (index / total_files) * 100
        progress_window.update_progress(progress_value)

    return success
