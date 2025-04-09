import logging
from pathlib import Path
from typing import List, Dict
import PyPDF2
from PyPDF2.generic import IndirectObject
from backend.imgRelated.decoder import decode_image
from backend.imgRelated.base64 import image_to_base64

from backend.imgRelated.text_from_img import extract_text_from_image


def extract_images(file_path: Path) -> List[Dict]:
    """
    Extracts images and associated text from the provided PDF file.

    Args:
        file_path (Path): The file path to the PDF document.

    Returns:
        List[Dict]: A list of dictionaries, each representing a page with grouped images.
    """

    pages = []

    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)

            for page_number, page in enumerate(reader.pages, 1):
                resources = page.get("/Resources")
                if isinstance(resources, IndirectObject):
                    resources = resources.get_object()

                if not resources or "/XObject" not in resources:
                    continue

                xObject = resources["/XObject"]
                if isinstance(xObject, IndirectObject):
                    xObject = xObject.get_object()

                page_images = {}
                image_count = 1

                for obj_name in xObject:
                    obj = xObject[obj_name]
                    if isinstance(obj, IndirectObject):
                        obj = obj.get_object()

                    if obj.get("/Subtype") == "/Image":
                        image = decode_image(obj)

                        if image is None:
                            logging.warning(f"Skipping a failed image on page {page_number}.")
                            continue

                        base64_image = image_to_base64(image)
                        extracted_text = extract_text_from_image(image)



                        page_images[f"image{image_count}"] = {
                            "base64 of image": base64_image,
                            "extracted text from image": extracted_text,
                        }
                        image_count += 1

                if page_images:
                    pages.append({
                        "page": f"page {page_number}",
                        **page_images
                    })

    except Exception as e:
        logging.error(f"Error extracting images from PDF {file_path}: {str(e)}")

    return pages
