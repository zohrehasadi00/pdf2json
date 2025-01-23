import pdfplumber
from pathlib import Path
from typing import List, Dict
from models.longformer_model import long_summarization

# Facebook's BART # limitation: 1024 token
# summarizer = SummarizationModel()


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
                            # Facebook's BART
                            # summary = summarizer.summarize(text, max_length=150, min_length=50)

                            # LED summarization # slow
                            # summary = led_summarization(text)

                            # Longformer summarization # better
                            summary = long_summarization(text)

                        except Exception as e:
                            print(e)
                            summary = "An error occurred and summary was not possible"
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
    return result
