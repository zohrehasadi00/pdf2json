import logging
from typing import Dict, List
from models.gpt4_summary import summarize_text
import pdfplumber

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_text_and_summarize(file_path) -> List[Dict]:
    """Extracts text from each page and summarizes it."""

    page_data = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            try:
                text = page.extract_text()
                if not text:
                    page_data.append({"page": page.page_number, "data": {"paragraphs": [], "sections": []}})
                    continue

                text = text.lower()
                paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
                summarized_paragraphs = []

                for paragraph in paragraphs:
                    try:
                        summary = summarize_text(paragraph)
                    except Exception as e:
                        logging.error(f"Error summarizing: {str(e)}")
                        summary = "Summarization failed"

                    summarized_paragraphs.append({"paragraph": paragraph, "summary": summary})

                page_data.append({"page": page.page_number, "data": {"paragraphs": summarized_paragraphs}})

            except Exception as e:
                logging.error(f"Error reading page {page.page_number}: {str(e)}")
                page_data.append({"page": page.page_number,
                                  "data": {"text": "Error reading page", "summary": "No summary available"}})

    return page_data
