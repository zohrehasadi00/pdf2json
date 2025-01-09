from pathlib import Path
from PIL import Image
from text_extractor import extract_text_and_summarize
from image_extractor import PdfImageTextExtractor


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
    result = {
        "Status": "Success",
        "Title": file_path.name,
        "Pages": []
    }

    try:
        pdf_image_extractor = PdfImageTextExtractor()
        extracted_pages = pdf_image_extractor.extract_images(file_path)

        for page in extracted_pages:
            page_number = page.get("PageNumber")
            images = page.get("Images", [])

            if not images:
                continue

            page_data = {
                "Page": f"Page {page_number}",
                "Images": []
            }

            for image in images:
                image_obj = image.get("Image")

                if not isinstance(image_obj, Image.Image):
                    continue

                try:
                    image_base64 = pdf_image_extractor.image_to_base64(image_obj)
                    extracted_text = pdf_image_extractor.extract_text_from_image(image_obj)

                    page_data["Images"].append({
                        "Base64": image_base64,
                        "ExtractedText": extracted_text
                    })
                except Exception as e:
                    page_data["Images"].append({
                        "Error": f"Error processing image: {str(e)}"
                    })

            result["Pages"].append(page_data)

    except Exception as e:
        result["Status"] = "Error"
        result["ErrorMessage"] = f"Error extracting images: {str(e)}"

    return result
