import logging
from PIL import Image
from models.tesseract_ocr_model import TesseractOcrModel
from models.base_ocr_model import BaseOcrModel


def extract_text_from_image(image: Image.Image) -> str:
    """
    Extracts text from an image using OCR.

    Args:
        image (Image.Image): The PIL Image object.

    Returns:
        str: The extracted text, or an empty string on failure.
    """
    ocr_model = TesseractOcrModel(BaseOcrModel)

    try:
        text = ocr_model.predict(image)
        text = text.replace("\n\n", "__")
        text = text.replace("\n", "")
        text = text.replace("%) Thieme Compliance", "No text found")
        return text
    except Exception as e:
        logging.error(f"Error extracting text from image: {str(e)}")
        return ""
