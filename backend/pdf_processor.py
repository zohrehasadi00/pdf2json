import pdfplumber
import logging
from pathlib import Path
from backend.text_extractor import extract_text_and_summarize
from backend.image_extractor import PdfImageTextExtractor
# import json
# import time
# import PyPDF2
# from typing import List
# from datetime import timedelta
# from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
extractor = PdfImageTextExtractor()


def combine_page_and_image_data(page_data, image_data):
    combined_data = []

    for page_entry in page_data:
        page_number = page_entry["page"]
        paragraphs = page_entry["data"]["paragraphs"]

        images_for_page = next(
            (img_entry for img_entry in image_data if img_entry["page"] == f"page {page_number}"),
            None
        )

        formatted_images = []
        if images_for_page:
            for key, image_info in images_for_page.items():
                if key.startswith("image"):
                    formatted_images.append({
                        "base64 of image": image_info["base64 of image"],
                        "image description": image_info["image description"],
                        "extracted text from image": image_info["extracted text from image"],
                        "related paragraph": image_info["related paragraph/s"],
                    })

        combined_data.append({
            "page": page_number,
            "paragraphs": paragraphs,
            "extracted images": formatted_images
        })

    return combined_data


def process_pdf(file_path: Path) -> dict:
    """Main function to process the entire PDF, extracting text and images in parallel."""
    # logging.info(f"Starting processing for PDF: {file_path}")
    # start_time = time.perf_counter()

    if not file_path.exists() or not file_path.is_file():
        # logging.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with pdfplumber.open(file_path) as pdf:
            page_data = []
            for page in pdf.pages:
                info = {"page": page.page_number, "data": extract_text_and_summarize(page)}
                page_data.append(info)

        image_data = extractor.extract_images(file_path, page_data)
        combined_data = combine_page_and_image_data(page_data, image_data)
        return {"status": "success", "title": file_path.name, "extracted data": combined_data}

    except Exception as e:
        # logging.error(f"Error processing the PDF: {str(e)}")
        return {"status": "failure", "error": str(e)}
