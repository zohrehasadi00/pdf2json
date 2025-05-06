import io
import fitz  # PyMuPDF
import logging
from PIL import Image
from models.gpt4_cleaning_text import cleaning
from models.gpt4_summary import summarize_text
from backend.imgRelated.base64 import image_to_base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from backend.imgRelated.text_from_img import extract_text_from_image

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)

def convert_pdf_to_images(pdf_path):
    pdf_document = fitz.open(pdf_path)
    images = []
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        # img.show()
        images.append((page_num + 1, img))
    return images


def summarize(extracted_text):
    text = extracted_text.strip()
    if len(text) < 10:
        return "text is short"

    cleaned = cleaning(text)
    return summarize_text(cleaned).lower() if len(cleaned) > 200 else "text is short"


def process_single_page(args):
    page_number, image = args
    try:
        base64_image = image_to_base64(image)
        extracted_text = extract_text_from_image(image)
        extracted_text = cleaning(extracted_text)
        logging.info(f"Page {page_number}: Image has been encoded and its text extracted.")
        return (page_number, base64_image, extracted_text)

    except Exception as e:
        logging.warning(f"Failed to process page {page_number}: {str(e)}")
        return None


def process_data(pdf_path):
    logging.info("Converting the PDF pages -> images")
    image_pages = convert_pdf_to_images(pdf_path)
    logging.info(f"{len(image_pages)} images has been created")

    image_data = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_single_page, (page_num, image))
                   for page_num, image in image_pages]

        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                image_data.append(result)

    page_images = {}

    with ThreadPoolExecutor() as executor:
        summary_futures = {
            executor.submit(summarize, text): (page_num, base64_img, text)
            for page_num, base64_img, text in image_data
        }

        for future in as_completed(summary_futures):
            page_num, base64_img, text = summary_futures[future]
            logging.debug(f"Processing page {page_num}...")

            try:
                summary = future.result()
                logging.info(f"Summary generated for page {page_num}.")

                page_images[f"Page{page_num}"] = {
                    "base64 of image": base64_img,
                    "extracted text from image": text,
                    "summary": summary
                }

            except Exception as e:
                logging.error(f"Error summarizing page {page_num}: {str(e)}")

    final_results = {
        f"Page{i}": page_images[f"Page{i}"]
        for i in range(1, len(image_pages) + 1)
        if f"Page{i}" in page_images
    }

    logging.info("Completed all tasks")
    return final_results
