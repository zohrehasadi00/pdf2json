import logging
from models.base_ocr_model import BaseOcrModel
from PIL import Image, ImageFilter, ImageEnhance
from models.tesseract_ocr_model import TesseractOcrModel


def preprocess_image(image: Image.Image) -> Image.Image:

    image = image.convert('L')  # Convert to grayscale
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(3.0)  # Increase contrast by a factor of 3
    image = image.point(lambda p: p > 128 and 255)   # Convert to black & white

    return image

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

        if text is None:
            return ""
        text = text.replace("\n", "").lower()
        return text
    except Exception as e:
        logging.error(f"Error extracting text from image: {str(e)}")
        return ""
