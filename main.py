# imports
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image
from pillow_heif import HeifImagePlugin  # noqa: F401  # Enables HEIF/HEIC support in Pillow

# welcome
print("Welcome to AnyF")

# finding the path for the image
image_path = Path(input("Enter the path of the image you want to convert: ").strip())

# checking if the path exists and is a file
if not (image_path.exists() and image_path.is_file()):
    print("Invalid file.")
    sys.exit(1)

print("Valid file.")

# detect the image format
try:
    result = subprocess.run(
        ["identify", "-format", "%m", str(image_path)],
        capture_output=True,
        text=True,
        timeout=60,
    )
except FileNotFoundError:
    print("ImageMagick is not installed or is not available in PATH.")
    sys.exit(1)
except subprocess.TimeoutExpired:
    print("ImageMagick took too long to identify the image.")
    sys.exit(1)

if result.returncode != 0:
    print("Could not identify image.")
    if result.stderr:
        print(result.stderr.strip())
    sys.exit(1)

input_format = result.stdout.strip()
print("Detected format:", input_format)

# image loading
img = None

try:
    with Image.open(image_path) as opened_image:
        img = opened_image.copy()
except (OSError, ValueError):
    print("Pillow cannot open this image. Trying ImageMagick...")

    with tempfile.TemporaryDirectory() as temp_folder:
        temp_png = Path(temp_folder) / "converted.png"

        try:
            result = subprocess.run(
                ["convert", str(image_path) + "[0]", str(temp_png)],
                capture_output=True,
                text=True,
                timeout=60,
            )
        except FileNotFoundError:
            print("ImageMagick is not installed or is not available in PATH.")
            sys.exit(1)
        except subprocess.TimeoutExpired:
            print("ImageMagick took too long to convert the image.")
            sys.exit(1)

        if result.returncode != 0:
            print("ImageMagick could not open this image.")
            if result.stderr:
                print(result.stderr.strip())
            sys.exit(1)

        try:
            with Image.open(temp_png) as converted:
                img = converted.copy()
        except (OSError, ValueError) as error:
            print("Could not open the image converted by ImageMagick.")
            print(error)
            sys.exit(1)

print("Image format:", input_format)
print("Image size:", img.size)
print("Image mode:", img.mode)

# asking which format you want to change the photo to
print("Which format do you want to convert the image to?")
print("1. PNG")
print("2. JPEG")
print("3. WEBP")
print("4. HEIF")
print("5. BMP")
print("6. TIFF")

image_format = input("Enter the number of the format you want to convert to: ").strip()

# conversion
if image_format == "1":
    print("Selected format: PNG")
    output_format = "PNG"
    extension = "png"
elif image_format == "2":
    print("Selected format: JPEG")
    output_format = "JPEG"
    extension = "jpg"
elif image_format == "3":
    print("Selected format: WEBP")
    output_format = "WEBP"
    extension = "webp"
elif image_format == "4":
    print("Selected format: HEIF/HEIC")
    output_format = "HEIF"
    extension = "heif"
elif image_format == "5":
    print("Selected format: BMP")
    output_format = "BMP"
    extension = "bmp"
elif image_format == "6":
    print("Selected format: TIFF")
    output_format = "TIFF"
    extension = "tiff"
else:
    print("You made a typo, try again.")
    sys.exit(1)

# conversion engine
output_dir = Path.home() / "Pictures"
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / f"{image_path.stem}_converted.{extension}"

# avoid silently overwriting an existing converted file
if output_path.exists():
    print(f"A file named {output_path.name} already exists.")
    overwrite = input("Overwrite it? (y/n): ").strip().lower()
    if overwrite != "y":
        print("Conversion cancelled.")
        sys.exit(1)

try:
    img.save(output_path, format=output_format)
except (OSError, ValueError) as error:
    print("Conversion failed.")
    print(error)
    sys.exit(1)

if not output_path.is_file():
    print("Conversion failed: output file was not created.")
    sys.exit(1)

print(f"Conversion successful. You can find the file here: {output_path}")
