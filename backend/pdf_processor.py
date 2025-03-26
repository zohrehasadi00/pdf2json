import logging
from pathlib import Path
from backend.normal_pdfs.text_extractor import extract_text_and_summarize
from backend.normal_pdfs.image_extractor import PdfImageTextExtractor
from models.check_pdf import check
from backend.scanned_pdfs.cid_pdf import process_data

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
extractor = PdfImageTextExtractor()


def combine_page_and_image_data(page_data, image_data):
    combined_data = []

    for page_entry in page_data:
        page_number = page_entry["page"]
        paragraphs = page_entry["data"]["paragraphs"]

        images_for_page = next((img_entry for img_entry in image_data if img_entry["page"] == f"page {page_number}"), None)

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

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        if check(file_path):
            return process_data(file_path)
        else:
            text_data = extract_text_and_summarize(file_path)
            image_data = extractor.extract_images(file_path, text_data)
            combined_data = combine_page_and_image_data(text_data, image_data)
            return {"status": "success", "title": file_path.name, "extracted data": combined_data}

    except Exception as e:
        return {"status": "failure", "error": str(e)}
