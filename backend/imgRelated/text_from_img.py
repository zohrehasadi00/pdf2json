import logging
from PIL import Image
from models.base_ocr_model import BaseOcrModel
from models.gpt4_cleaning_text import cleaning
from models.tesseract_ocr_model import TesseractOcrModel
from backend.imgRelated.preprocess import preprocess_image



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
        image = preprocess_image(image)
        text = ocr_model.predict(image)
        text = cleaning(text).replace("\n", "").replace("%) Thieme Compliance", "No text found")
        return text
    except Exception as e:
        logging.error(f"Error extracting text from image: {str(e)}")
        return ""
