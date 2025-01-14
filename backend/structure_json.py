from pathlib import Path
from PIL import Image
from backend.text_extractor_old import extract_text_and_summarize
from backend.image_extractor import PdfImageTextExtractor
import logging


def process_pdf_text_only(file_path: Path) -> dict:
    """
    Process PDF to extract text and summaries
    Returns structured JSON output
    """
    try:
        text_data = extract_text_and_summarize(file_path)

        if not text_data:
            return {
                "Status": "Error",
                "Title": file_path.name,
                "ErrorMessage": "No text data found in the PDF."
            }

        result = {
            "Status": "Success",
            "Title": file_path.name,
            "Pages": [
                {
                    "Page": f"Page {page['PageNumber']}",
                    "Text": page["Text"],
                    "Summary": page["Summary"],
                }
                for page in text_data
            ],
        }

        return result

    except Exception as e:
        return {
            "Status": "Error",
            "Title": file_path.name,
            "ErrorMessage": f"Error extracting text: {str(e)}"
        }


def process_pdf_image_only(file_path: Path) -> dict:
    """
    Processes a PDF file to extract images and text from images, returning a structured JSON response.

    Args:
        file_path (Path): Path to the PDF file.

    Returns:
        dict: A dictionary containing the extraction status, title, and page data.
    """
    try:
        # Initialize the image text extractor
        pdf_image_extractor = PdfImageTextExtractor()

        # Extract images and text from the PDF
        extracted_pages = pdf_image_extractor.extract_images(file_path)

        # Build JSON response
        result = {
            "Status": "Success",
            "Title": file_path.name,
            "Pages": [
                {
                    "Page": f"Page {page.get('PageNumber')}",
                    "Images": [
                        {
                            "Base64": image.get("Base64Image"),
                            "ExtractedText": image.get("ExtractedText")
                        }
                        for image in page.get("Images", [])
                    ],
                }
                for page in extracted_pages
            ],
        }

    except Exception as e:
        logging.error(f"Error processing PDF file: {file_path}")
        result = {
            "Status": "Error",
            "ErrorMessage": f"Error extracting images: {str(e)}",
            "Title": file_path.name,
            "Pages": [],
        }

    return result


pdf_path = Path(r"C:/Users/zohre/OneDrive/Desktop/bachelorArbeit/pdf_example/The_Basics_of_Anesthesia_7th_Edition.pdf")
process_pdf_text_only(pdf_path)
print("********************************************************************")
print("********************************************************************")
print("********************************************************************")
(process_pdf_image_only(pdf_path))
