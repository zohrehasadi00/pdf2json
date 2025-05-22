import logging


# Suppress pdfminer CropBox warnings
class SuppressCropBoxWarning(logging.Filter):
    def filter(self, record):
        return "CropBox missing from /Page" not in record.getMessage()


logging.getLogger("pdfminer").addFilter(SuppressCropBoxWarning())
logging.getLogger("pdfminer").setLevel(logging.ERROR)

import pdfplumber
from typing import Dict, List
from langdetect import detect
from models.gpt4_summary import summarize_text
from models.gpt4_cleaning_text import cleaning
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from models.nlp_paragraph_detection import segment_paragraphs_textrank

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)


def process_page(page_num: int, page_text: str) -> Dict:
    try:
        if not page_text:
            return {"page": page_num, "data": {"paragraphs": []}}

        text = cleaning(page_text).replace("–", " ").replace("- ", " ").replace(".", " ") \
            .replace(":", " ").replace("/", " ").lower().replace("\n", " ") \
            .replace("  ", " ").strip()

        logging.info(f"Text in page {page_num} has been")
        logging.info(f"_______________ extracted")
        logging.info(f"_______________ cleaned")

        language = detect(text)
        paragraphs = segment_paragraphs_textrank(text, language)
        logging.info(f"_______________ divided into paragraphs")
        summarized_paragraphs = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_paragraph = {
                executor.submit(summarize_paragraph, paragraph): paragraph for paragraph in paragraphs
            }

            logging.info("_______________ And summarized")

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

        return {
            "page": page_num,
            "data": {"paragraphs": summarized_paragraphs}
        }

    except Exception as e:
        logging.error(f"Error reading page {page_num}: {str(e)}")
        return {
            "page": page_num,
            "data": {"text": "Error reading page", "summary": "No summary available"}
        }


def extract_text_and_summarize(file_path) -> List[Dict]:
    """Extracts text from each page and summarizes it using parallel processing."""
    page_data = []

    with pdfplumber.open(file_path) as pdf:
        pages = [(page.page_number, page.extract_text()) for page in pdf.pages]

    with ProcessPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_page, num, text) for num, text in pages]

        for future in as_completed(futures):
            page_data.append(future.result())

    page_data.sort(key=lambda x: x['page'])

    return page_data


def summarize_paragraph(paragraph: str) -> str:
    """Helper function to get the summarization."""
    try:
        text = paragraph.lower()
        return summarize_text(text).lower() if len(text) > 200 else "Text is short."

    except Exception as e:
        logging.error(f"Error summarizing paragraph: {str(e)}")
        return "Summarization failed"
