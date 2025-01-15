from pathlib import Path
from backend.text_extractor import extract_text_and_summarize
from backend.image_extractor import PdfImageTextExtractor
import logging
import time
import json
from datetime import timedelta


def process_pdf_text_only(file_path: Path) -> dict:
    """
    Process PDF to extract text and summaries
    Returns structured JSON output
    """
    # starttime = time.perf_counter()
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

    except Exception as e:
        return {
            "Status": "Error",
            "Title": file_path.name,
            "ErrorMessage": f"Error extracting text: {str(e)}"
        }

    # duration = timedelta(seconds=time.perf_counter() - starttime)
    # print('extracting the text took: ', duration)
    # formated_result = "\n".join(json.dumps(item, indent=4) for item in result)
    formated_result = json.dumps(result, indent=4)
    print(formated_result)
    return result


def process_pdf_image_only(file_path: Path) -> dict:
    """
    Processes a PDF file to extract images and text from images, returning a structured JSON response.

    Args:
        file_path (Path): Path to the PDF file.

    Returns:
        dict: A dictionary containing the extraction status, title, and page data.
    """
    try:
        pdf_image_extractor = PdfImageTextExtractor()
        extracted_pages = pdf_image_extractor.extract_images(file_path)
        f = json.dumps(extracted_pages, indent=4)
        print(f)
        print("''''''''''''''''''''''''''''''''''''''''''''''''")
        result = {
            "Status": "Success",
            "Title": file_path.name,
            "Pages": [
                {
                    "Page": page.get("Page"),
                    **{
                        key: value
                        for key, value in page.items() if key.startswith("image")
                    }
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

    formatted_result = json.dumps(result, indent=4)
    print(formatted_result)
    return result


# pdf_path = Path(r"C:/Users/zohre/OneDrive/Desktop/bachelorArbeit/pdf_example/The_Basics_of_Anesthesia_7th_Edition.pdf") # not bad
# # pdf_path = Path(r"C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\pdf_example\test.pdf") #good
# # pdf_path = Path(r"C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\pdf_example\IntroductionToAnaesthesia.pdf")
# process_pdf_text_only(pdf_path)
# print("********************************************************************")
# print("********************************************************************")
# print("********************************************************************")
# process_pdf_image_only(pdf_path)
