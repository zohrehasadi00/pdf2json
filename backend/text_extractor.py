import os
import json
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import pdfplumber
from pathlib import Path
from typing import List, Dict
from models.longformer_model import summarization
import logging
import time
from datetime import timedelta
from concurrent.futures import ProcessPoolExecutor  # Change to ProcessPoolExecutor
import multiprocessing

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_text_and_summarize(page, page_no) -> Dict:
    logging.info(f"Starting text extraction and summarization for: {page_no}")
    start_time = time.perf_counter()

    try:
        text = page.extract_text()
        if text:
            try:
                summary = summarization(text)
            except Exception as e:
                logging.error(f"Error summarizing text on page {page_no}: {str(e)}")
                summary = "An error occurred and summary was not possible"
        else:
            logging.warning(f"No text found on page {page_no}")
            text = "No text available"
            summary = "No summary available"

        duration = timedelta(seconds=time.perf_counter() - start_time)
        logging.info(f"Summarization took: {duration}")
    except Exception as page_error:
        logging.error(f"Error extracting text or reading page {page_no}: {str(page_error)}")
        text = f"Error reading page: {page_error}"
        summary = "No summary available"
    return {"PageNumber": page_no, "Text": text, "Summary": summary}
