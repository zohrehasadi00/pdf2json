import io
import fitz
import logging
from PIL import Image
from models.gpt4_cleaning_text import cleaning
from models.gpt4_summary import summarize_text
from concurrent.futures import ThreadPoolExecutor
from backend.imgRelated.base64 import image_to_base64
from backend.imgRelated.text_from_img import extract_text_from_image


def convert_pdf_to_images(pdf_path):
    pdf_document = fitz.open(pdf_path)
    images = []

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        images.append(img)

    return images


def process_text(extracted_text):

    result = cleaning(extracted_text)
    result = result.replace("\n\n", "").replace("\n", "")
    summary = summarize_text(result)
    return result, summary


def process_data(pdf_path):
    images = convert_pdf_to_images(pdf_path)
    logging.info("All pages of the PDF have been converted to images ...")

    page_images = {}
    image_count = 1

    image_data = []
    logging.info("Converting images to base64 encoding and extracting their raw texts ...")

    for image in images:
        base64_image = image_to_base64(image)
        extracted_text = extract_text_from_image(image)
        image_data.append((image_count, base64_image, extracted_text))
        image_count += 1

    logging.info("Cleaning Texts and summarizing them ...")
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_text, data[2]): data for data in image_data}

        logging.info("Combining the data ...")
        for future in futures:
            image_count, base64_image, _ = futures[future]
            result, summary = future.result()

            page_images[f"Page{image_count}"] = {
                "base64 of image": base64_image,
                "extracted text from image": result,
                "summary": summary
            }

    return page_images
