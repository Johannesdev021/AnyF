#imports
from PIL import Image
from pathlib import  Path
from pillow_heif import HeifImagePlugin
import os
import sys
import subprocess
import tempfile
import rawpy
import cairosvg

#welcome
print("Welcome to AnyF")

#finding the path for the image
image_path = input("Enter the path of the image you want to convert:")
image_path = Path(image_path)

# Checking if the path exists and is a file
if image_path.exists() and image_path.is_file():
    print("Valid file.")

    # Detect the image format
    result = subprocess.run(
        ["identify", "-format", "%m", str(image_path)],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        input_format = result.stdout.strip()
        print("Detected format:", input_format)
    else:
        print("Could not identify image.")
        sys.exit(1)

else:
    print("Invalid file.")
    sys.exit(1)

#image "data"
# Image loading
try:
    img = Image.open(image_path)
    img.load()

except OSError:
    print("Pillow cannot open this image. Trying ImageMagick...")

    with tempfile.TemporaryDirectory() as temp_folder:

        temp_png = Path(temp_folder) / "converted.png"

        result = subprocess.run(
            ["convert", f"{image_path}[0]", str(temp_png)],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print("ImageMagick could not open this image.")
            print(result.stderr)
            sys.exit(1)

        with Image.open(temp_png) as converted:
            img = converted.copy()


print("Image format:", input_format)
print("Image size:", img.size)
print("Image mode:", img.mode)

#asking which format you wanna change the photo to
print("Which format do you want to convert the image to?")
print("1. PNG")
print("2. JPEG")
print("3. WEBP")
print("4. HEIF")
print("5. BMP")
print("6. TIFF")

image_format = input("Enter the number of the format you want to convert to.")

#conversion
#PNG
if image_format == "1":
    print("Selected format: PNG")
    output_format = "PNG"
    extension = "png"

#JPG
elif image_format == "2":
    print("Selected format: JPEG")
    output_format = "JPEG"
    extension = "jpeg"

#WEBP
elif image_format == "3":
    print("Selected format: WEBP")
    output_format = "WEBP"
    extension = "webp"

#HEIF
elif image_format == "4":
    print("Selected format: HEIF/HEIC")
    output_format = "HEIF"
    extension = "heif"

#BMP
elif image_format =="5":
    print("Selected format: BMP")
    output_format = "BMP"
    extension = "bmp"

#TIFF
elif image_format =="6":
    print("Selected format: TIFF")
    output_format = "TIFF"
    extension = "tiff"

#error handling
else:
    print("You made a typo, try again.")

#Conversion engine
output_dir = Path.home() / "Pictures"

output_path = output_dir / f"{image_path.stem}_converted.{extension}"
img.save(output_path, format=output_format)
print("convertication succesfull, you can find the file inside the Photos folder.")