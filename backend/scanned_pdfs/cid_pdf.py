import os
import fitz
from PIL import Image
import io
from backend.imgRelated.base64 import image_to_base64
from backend.imgRelated.text_from_img import extract_text_from_image
from models.gpt4_cleaning_text import cleaning


def convert_pdf_to_images(pdf_path):
    pdf_document = fitz.open(pdf_path)
    images = []

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        images.append(img)

    return images

def process_data(pdf_path):
    images = convert_pdf_to_images(pdf_path)

    page_images = {}
    image_count = 1
    for image in images:
        base64_image = image_to_base64(image)
        extracted_text = extract_text_from_image(image)
        result = cleaning(extracted_text)

        page_images[f"Page{image_count}"] = {
            "base64 of image": base64_image,
            "extracted text from image": result
        }
        image_count += 1

    file_name = os.path.basename(pdf_path)
    return {"Status": "Success", "title": file_name, "extracted data": page_images}
