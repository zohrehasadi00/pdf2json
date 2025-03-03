import pdfplumber
from pathlib import Path
import json
import logging
import time
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor
from backend.text_extractor import extract_text_and_summarize
from backend.image_extractor import PdfImageTextExtractor
from multiprocessing import Pool   # for I/O bound
from concurrent.futures import ProcessPoolExecutor   #if either is CPU-Bound


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
extractor = PdfImageTextExtractor()


# Process each page concurrently
def process_page_concurrently(page, page_no):
    """Extract text and summarize, and extract images concurrently."""
    # Use ThreadPoolExecutor to run text extraction and image extraction in parallel
    with ThreadPoolExecutor() as executor:
        text_future = executor.submit(extract_text_and_summarize, page, page_no)
        #image_future = executor.submit(extractor.extract_images, page, page_no)

    # Multi-processing (For CPU-Bound)
    # with Pool() as pool:
    #     texts = pool.map(extract_text_and_summarize, page, page_no)
    #     images = pool.map(extractor.extract_images, page)

        text_data = text_future.result()
        #extracted_images = image_future.result()

        return {
            "Page": f"Page {page_no}",
            "Text": text_data["Text"],
            "Summary": text_data["Summary"] #, "Images": extracted_images
        }


# Main function to process the entire PDF and parallelize tasks
def process_pdf(file_path: Path) -> dict:
    """Main function to process the entire PDF, extracting text and images in parallel."""
    logging.info(f"Starting processing for PDF: {file_path}")
    start_time = time.perf_counter()

    result = {"Status": "Success", "Title": file_path.name, "Pages": []}

    if not file_path.exists() or not file_path.is_file():
        logging.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with pdfplumber.open(file_path) as pdf:
            if not pdf.pages:
                logging.error(f"The PDF file '{file_path}' has no pages.")
                raise ValueError(f"The PDF file '{file_path}' has no pages.")

            # Use ThreadPoolExecutor to process pages concurrently
            with ThreadPoolExecutor() as executor:
                # Parallel processing for all pages
                results = list(executor.map(process_page_concurrently, pdf.pages, range(1, len(pdf.pages) + 1)))

            #image_results = extractor.extract_images(file_path)
            result["Pages"].extend(results)

        duration = timedelta(seconds=time.perf_counter() - start_time)
        logging.info(f"Processing took: {duration}")

    except Exception as e:
        logging.error(f"Error processing the PDF: {str(e)}")
        result["Status"] = "Failure"
        result["Error"] = str(e)

    return result


result = process_pdf(Path(r"C:\Users\zohre\bachelorT\MediLink\example\sample_pdfs\IntroductionToAnaesthesia.pdf"))
print(json.dumps(result, indent=4))
