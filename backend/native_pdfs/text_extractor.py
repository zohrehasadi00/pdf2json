import logging
import pdfplumber
from typing import Dict, List
from langdetect import detect
from models.gpt4_summary import summarize_text
from models.gpt4_cleaning_text import cleaning
from concurrent.futures import ThreadPoolExecutor, as_completed
from models.nlp_paragraph_detection import segment_paragraphs_textrank

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_text_and_summarize(file_path) -> List[Dict]:
    """Extracts text from each page and summarizes it."""

    page_data = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            try:
                text = page.extract_text()
                if not text:
                    page_data.append({"page": page.page_number, "data": {"paragraphs": []}})
                    continue

                text = text.lower().replace("\n", "")
                language = detect(text)
                paragraphs = segment_paragraphs_textrank(text, language)
                summarized_paragraphs = []

                with ThreadPoolExecutor() as executor:
                    future_to_paragraph = {
                        executor.submit(summarize_paragraph, paragraph): paragraph for paragraph in paragraphs
                    }

                    for future in as_completed(future_to_paragraph):
                        try:
                            summary = future.result()
                            summarized_paragraphs.append({
                                "paragraph": future_to_paragraph[future],
                                "summary": summary
                            })
                        except Exception as e:
                            logging.error(f"Error summarizing: {str(e)}")
                            summarized_paragraphs.append({
                                "paragraph": future_to_paragraph[future],
                                "summary": "Summarization failed"
                            })

                page_data.append({
                    "page": page.page_number,
                    "data": {"paragraphs": summarized_paragraphs}
                })

            except Exception as e:
                logging.error(f"Error reading page {page.page_number}: {str(e)}")
                page_data.append({
                    "page": page.page_number,
                    "data": {"text": "Error reading page", "summary": "No summary available"}
                })

    return page_data


def summarize_paragraph(paragraph: str) -> str:
    """Helper function to get the summarization."""
    try:
        text = cleaning(paragraph)
        text = text.lower()
        if len(text) > 150:
            summy = summarize_text(text).lower()
            return summy
        else:
            return text
    except Exception as e:
        logging.error(f"Error summarizing paragraph: {str(e)}")
        return "Summarization failed"
