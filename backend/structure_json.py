from pathlib import Path
from backend.text_extractor import extract_text_and_summarize
from backend.image_extractor import PdfImageTextExtractor
import logging


def process_pdf(file_path: Path) -> dict:
    try:
        text_data = extract_text_and_summarize(file_path)

        pdf_image_extractor = PdfImageTextExtractor()
        extracted_pages = pdf_image_extractor.extract_images(file_path)

        if not text_data:
            return {
                "Status": "Error",
                "Title": file_path.name,
                "ErrorMessage": "No text data found in the PDF."
            }

        result = {
            "Status": "Success",
            "Title": file_path.name,
            "Pages": []
        }

        for idx, page in enumerate(text_data):
            page_data = {
                "Page": f"Page {page['PageNumber']}",
                "Text": page["Text"],
                "Summary": page["Summary"],
                "Images": []
            }

            if idx < len(extracted_pages):
                images = extracted_pages[idx]
                for img_key in images:
                    if img_key.startswith("image"):
                        base64_image_data = images[img_key]
                        page_data["Images"].append({
                            "Base64Image": base64_image_data,
                            "Extracted text from image": images.get(f"image_text_{img_key}", "")
                        })

            result["Pages"].append(page_data)

        return result

    except Exception as e:
        logging.error(f"Error processing PDF file: {file_path}")
        return {
            "Status": "Error",
            "Title": file_path.name,
            "ErrorMessage": f"Error processing PDF: {str(e)}",
            "Pages": []
        }
