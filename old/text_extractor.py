import PyPDF2
from pathlib import Path
from typing import List, Dict
from models.summarization_model import SummarizationModel
import json

summarizer = SummarizationModel()


def extract_text_and_summarize(file_path: Path) -> List[Dict]:
    """
    Extract text and summarize it for each page of the PDF.
    """
    result = []
    try:
        with (open(file_path, "rb") as pdf_file):
            reader = PyPDF2.PdfReader(pdf_file)
            if not reader.pages:
                raise ValueError(f"The PDF file '{file_path}' has no pages.")

            for page_no, page in enumerate(reader.pages, start=1):
                if page_no == 2:
                    a = page.extract_text()
                    b = summarizer.summarize(a, max_length=150, min_length=50)

                try:
                    text = page.extract_text()
                    if text:
                        try:
                            summary = summarizer.summarize(text, max_length=150, min_length=50)
                        except Exception as e:
                            print(e)
                            summary = "summary not possible - error occurred"

                    else:
                        text = "No text available"
                        summary = "No summary available"
                    result.append({
                        "PageNumber": page_no,
                        "Text": text,
                        "Summary": summary,
                    })
                except Exception as page_error:
                    text = f"Error reading page: {page_error}"
                    summary = "No summary available"
    except Exception as e:
        raise Exception(f"Error extracting text: {str(e)}")
    return result
