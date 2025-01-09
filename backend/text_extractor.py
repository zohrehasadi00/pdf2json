import PyPDF2
from pathlib import Path
from typing import List, Dict
from models.summarization_model import SummarizationModel

summarizer = SummarizationModel()


def extract_text_and_summarize(file_path: Path) -> List[Dict]:
    """
    Extract text and summarize it for each page of the PDF.
    """
    result = []
    try:
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)

            for page_no, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if text:
                    cleaned_text = " ".join(text.replace("\n", " ").split())
                    if cleaned_text:  # Check if cleaned text is non-empty
                        try:
                            summary = summarizer.summarize(cleaned_text, max_length=150, min_length=50)
                        except IndexError as e:
                            summary = f"Error during summarization: {str(e)}"
                    else:
                        summary = "No text available to summarize."
                else:
                    summary = "No text found on this page."

                result.append({
                    "PageNumber": page_no,
                    "Text": cleaned_text,
                    "Summary": summary,
                })
    except Exception as e:
        raise Exception(f"Error extracting text: {str(e)}")

    return result
