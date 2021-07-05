from fpdf import FPDF
from PIL import Image
import click

from pathlib import Path
import os


def get_images(directory):
    """Return a list with all the images in <directory>."""
    imagelist = []  # Contains the list of all images to be converted to PDF.
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in [f for f in filenames if f.endswith(".jpg")]:
            full_path = str(Path.joinpath(dirpath, filename))
            imagelist.append(full_path)

    imagelist.sort()  # Sort the images by name.
    return imagelist


def fix_landscape(imglist):
    """Rotate any landscape mode image if present."""
    for i in range(0, len(imglist)):
        im1 = Image.open(imglist[i])  # Open the image.
        width, height = im1.size  # Get the width and height of that image.
        if width > height:
            im2 = im1.transpose(
                Image.ROTATE_270
            )  # If width > height, rotate the image.
            os.remove(imglist[i])  # Delete the previous image.
            im2.save(imglist[i])  # Save the rotated image.


def make_pdf(directory, name, imglist):
    """Convert <imglist> into a PDF and saves it in <directory> as <name>."""
    pdf = FPDF()
    for image in imglist:
        pdf.add_page()
        pdf.image(
            image, 0, 0, 210, 297
        )  # 210 and 297 are the dimensions of an A4 size sheet.

    pdf.output(directory + name, "F")  # Save the PDF.


@click.command()
@click.argument("dirpath")
@click.argument("name")
def main(dirpath, name):
    """Merge every '.jpg' file in DIRPATH into a single PDF called NAME."""
    imagelist = get_images(dirpath)

    for imgpath in imagelist:
        print(imgpath)

    print(f"[✓] Found {len(imagelist)} '.jpg' files.")
    fix_landscape(imagelist)

    print(f"[i] Generating PDF...")
    make_pdf(dirpath, name, imagelist)
    print(f"[✓] Done!")


if __name__ == "__main__":
    main()  # Run the script.
