import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import pdfplumber
from pathlib import Path
import logging
import time
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor
from backend.text_extractor import extract_text_and_summarize
from backend.image_extractor import PdfImageTextExtractor

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
extractor = PdfImageTextExtractor()


def process_pdf(file_path: Path) -> dict:
    """Main function to process the entire PDF, extracting text and images in parallel."""
    logging.info(f"Starting processing for PDF: {file_path}")
    start_time = time.perf_counter()

    result = {"Status": "Success", "Title": file_path.name, "Pages": []}

    if not file_path.exists() or not file_path.is_file():
        logging.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with pdfplumber.open(file_path) as pdf:
            if not pdf.pages:
                logging.error(f"The PDF file '{file_path}' has no pages.")
                raise ValueError(f"The PDF file '{file_path}' has no pages.")
            with ThreadPoolExecutor() as executor:
                text_results = list(executor.map(
                    lambda args: {
                        "Page": f"Page {args[1]}",
                        **executor.submit(extract_text_and_summarize, *args).result()
                    },
                    zip(pdf.pages, range(1, len(pdf.pages) + 1))
                ))

        image_results = extractor.extract_images(file_path)
        merged_pages = []
        for text_page in text_results:
            image_page = next((p for p in image_results if p["Page"] == text_page["Page"]), None)
            if image_page:
                merged_pages.append({**text_page, **image_page})
            else:
                merged_pages.append(text_page)  # Keep text-only pages

        result["Pages"].extend(merged_pages)
        duration = timedelta(seconds=time.perf_counter() - start_time)
        logging.info(f"Processing the text took: {duration}")

    except Exception as e:
        logging.error(f"Error processing the PDF: {str(e)}")
        result["Status"] = "Failure"
        result["Error"] = str(e)

    return result
