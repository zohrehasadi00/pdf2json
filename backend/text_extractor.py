import pdfplumber
from pathlib import Path
import json
from typing import List, Dict
from models.summarization_model import SummarizationModel

summarizer = SummarizationModel()


def extract_text_and_summarize(file_path: Path) -> List[Dict]:
    result = []

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with pdfplumber.open(file_path) as pdf:

            if not pdf.pages:
                raise ValueError(f"The PDF file '{file_path}' has no pages.")

            for page_no, page in enumerate(pdf.pages, start=1):
                try:
                    text = page.extract_text()
                    if text:
                        try:
                            summary = summarizer.summarize(text, max_length=130, min_length=50)
                        except Exception as e:
                            print(e)
                            summary = "Was not possible"
                    else:
                        text = "No text available"
                        summary = "No summary available"
                except Exception as page_error:
                    text = f"Error reading page: {page_error}"
                    summary = "No summary available"

                result.append({
                    "PageNumber": page_no,
                    "Text": text,
                    "Summary": summary,
                })

    except Exception as e:
        raise Exception(f"Error extracting text: {str(e)}")

    formated_result = "\n".join(json.dumps(item, indent=4) for item in result)
    print(formated_result)

    return result
#pdf_path = Path(r"C:/Users/zohre/OneDrive/Desktop/bachelorArbeit/pdf_example/The_Basics_of_Anesthesia_7th_Edition.pdf")
#output = extract_text_and_summarize(pdf_path)
## TODO: remove formated_result