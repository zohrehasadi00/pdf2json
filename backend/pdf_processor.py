# import os

# os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import pdfplumber
import logging
import json
# import PyPDF2
from pathlib import Path

# import time
# from typing import List
# from datetime import timedelta
# from concurrent.futures import ThreadPoolExecutor
from backend.text_extractor import extract_text_and_summarize
from backend.image_extractor import PdfImageTextExtractor

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
extractor = PdfImageTextExtractor()


def combine_page_and_image_data(page_data, image_data):
    combined_data = []

    for page_entry in page_data:
        page_number = page_entry["page"]
        paragraphs = page_entry["data"]["paragraphs"]

        images_for_page = next(
            (img_entry for img_entry in image_data if img_entry["Page"] == f"Page {page_number}"),
            None
        )

        formatted_images = []
        if images_for_page:
            for key, image_info in images_for_page.items():
                if key.startswith("image"):
                    formatted_images.append({
                        "Base64 of Image": image_info["Base64 of Image"],
                        "Image Description": image_info["Image Description"],
                        "Extracted Text From Image": image_info["Extracted Text From Image"],
                        "Related Paragraph": image_info["Related paragraph/s"],
                    })

        combined_data.append({
            "Page": page_number,
            "Paragraphs": paragraphs,
            "Extracted Images": formatted_images
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
        return {"Status": "Success", "Title": file_path.name, "Combined Data": combined_data}
        # with pdfplumber.open(file_path) as pdf:
        #     if not pdf.pages:
        #         # logging.error(f"The PDF file '{file_path}' has no pages.")
        #         raise ValueError(f"The PDF file '{file_path}' has no pages.")
        #     with ThreadPoolExecutor() as executor:
        #         text_results = list(executor.map(
        #             lambda args: {
        #                 "Page": f"Page {args[1]}",
        #                 **executor.submit(extract_text_and_summarize, *args).result()
        #             },
        #             zip(pdf.pages, range(1, len(pdf.pages) + 1))
        #         ))

        # image_results = extractor.extract_images(file_path)
        # merged_pages = []
        # for text_page in text_results:
        #     image_page = next((p for p in image_results if p["Page"] == text_page["Page"]), None)
        #     if image_page:
        #         merged_pages.append({**text_page, **image_page})
        #     else:
        #         merged_pages.append(text_page)  # Keep text-only pages
        # result["Pages"].extend(merged_pages)
        # duration = timedelta(seconds=time.perf_counter() - start_time)
        # logging.info(f"Processing the text took: {duration}")

    except Exception as e:
        # logging.error(f"Error processing the PDF: {str(e)}")
        return {"Status": "Failure", "Error": str(e)}


# fun = process_pdf(file_path=Path(r""))
# print(json.dumps(fun, indent=4))
