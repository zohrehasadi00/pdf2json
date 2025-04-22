import logging
from pathlib import Path
from backend.check_pdf import check
from backend.scanned_pdfs.cid_pdf import process_data
from backend.native_pdfs.image_extractor import extract_images
from backend.native_pdfs.text_extractor import extract_text_and_summarize
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def combine_page_and_image_data(page_data, img_data):
    combined_data = []

    for page_entry in page_data:
        page_number = page_entry["page"]
        paragraphs = page_entry["data"]["paragraphs"]

        images_for_page = next((img_entry for img_entry in img_data if img_entry["page"] == f"page {page_number}"), None)

        formatted_images = []
        if images_for_page:
            for key, image_info in images_for_page.items():
                if key.startswith("image"):
                    formatted_images.append({
                        "base64 of image": image_info["base64 of image"],
                        "extracted text from image": image_info["extracted text from image"]
                    })

        combined_data.append({
            "page": page_number,
            "paragraphs": paragraphs,
            "extracted images": formatted_images
        })

    return combined_data


def process_pdf(file_path: Path) -> dict:
    """Main function to process the entire PDF, extracting text and images in parallel."""

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        logging.info("Checking PDF's kind ... ")
        if check(file_path):
            logging.info("PDF is scanned. Using OCR ... ")
            collected_data = process_data(file_path)

        else:
            logging.info("It is a native PDF ... ")

            with ThreadPoolExecutor(max_workers=4) as executor:
                future_text = executor.submit(extract_text_and_summarize, file_path)
                future_images = executor.submit(extract_images, file_path)

                text_data = future_text.result()
                image_data = future_images.result()

            logging.info("Combining the data ...")
            collected_data = combine_page_and_image_data(text_data, image_data)

        return {"status": "success", "title": file_path.name, "extracted data": collected_data}

    except Exception as e:
        return {"status": "failure", "error": str(e)}
