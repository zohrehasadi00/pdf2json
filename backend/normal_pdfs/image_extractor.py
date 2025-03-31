import PyPDF2
import logging
from pathlib import Path
from typing import List, Dict
# from models.blip_model import BlipModel
# from models.base_ocr_model import BaseOcrModel
from backend.imgRelated.decoder import decode_image
from backend.imgRelated.base64 import image_to_base64
# from sentence_transformers import SentenceTransformer
# from models.tesseract_ocr_model import TesseractOcrModel
# from backend.imgRelated.connectionToImg import visualLink
from backend.imgRelated.text_from_img import extract_text_from_image


def extract_images(file_path: Path) -> List[Dict]:  # , page_data: List[dict]) -> List[Dict]:
    """
    Extracts images and associated text from the provided PDF file.
    Args:
        file_path (Path): The file path to the PDF document.
        # page_data (List[dict]): List of all paragraphs from pages
    Returns:
        List[Dict]: A list of dictionaries, each representing a page with grouped images.
    """
    # logging.info("Start processing images and the data of the pdf")
    # start_time = time.perf_counter()
    pages = []
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)

            for page_number, page in enumerate(reader.pages, 1):
                resources = page.get("/Resources")

                if not resources or "/XObject" not in resources:
                    continue

                xObject = resources["/XObject"].get_object()
                page_images = {}
                image_count = 1

                for obj_name in xObject:
                    obj = xObject[obj_name]

                    if obj.get("/Subtype") == "/Image":
                        image = decode_image(obj)

                        if image is None:
                            # logging.warning(f"Skipping a failed image on page {page_number}.")
                            continue

                        base64_image = image_to_base64(image)
                        extracted_text = extract_text_from_image(image)
                        # match = visualLink(image, page_data, page_number)
                        page_images[f"image{image_count}"] = {
                            "base64 of image": base64_image,
                            "extracted text from image": extracted_text,
                            # "related paragraph/s": match
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
