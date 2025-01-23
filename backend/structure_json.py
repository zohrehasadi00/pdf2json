from pathlib import Path
from backend.text_extractor import extract_text_and_summarize
from backend.image_extractor import PdfImageTextExtractor
import logging
import json
import time
from datetime import timedelta


def process_pdf(file_path: Path) -> dict:
    starttime = time.perf_counter()
    try:
        text_data = extract_text_and_summarize(file_path)

        pdf_image_extractor = PdfImageTextExtractor()
        extracted_images = pdf_image_extractor.extract_images(file_path)
        extracted_videos = []

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

            if idx < len(extracted_images):
                images = extracted_images[idx]
                for img_key in images:
                    if img_key.startswith("image"):
                        base64_image_data = images[img_key]
                        page_data["Images"].append({
                            "Base64Image": base64_image_data,
                            "Extracted text from image": images.get(f"image_text_{img_key}", "")
                        })

            result["Pages"].append(page_data)

        duration = timedelta(seconds=time.perf_counter() - starttime)
        print('Summarization took: ', duration)
        formated_result = json.dumps(result, indent=4)
        print(formated_result)
        return result

    except Exception as e:
        logging.error(f"Error processing PDF file: {file_path}")
        return {
            "Status": "Error",
            "Title": file_path.name,
            "ErrorMessage": f"Error processing PDF: {str(e)}",
            "Pages": []
        }


pdf_path = Path(r"C:/Users/zohre/OneDrive/Desktop/bachelorArbeit/pdf_example/The_Basics_of_Anesthesia_7th_Edition.pdf") # not bad
# pdf_path = Path(r"C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\pdf_example\test.pdf") #good
# # pdf_path = Path(r"C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\pdf_example\IntroductionToAnaesthesia.pdf")
process_pdf(pdf_path)
