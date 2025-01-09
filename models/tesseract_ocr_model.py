from pytesseract import image_to_string
from PIL import Image
from models.base_ocr_model import BaseOcrModel


class TesseractOcrModel(BaseOcrModel):
    """Implementation of the OCR model using Tesseract."""

    def __init__(self, base_model_class):
        if not issubclass(base_model_class, BaseOcrModel):
            raise ValueError("Base model must inherit from BaseOcrModel.")
        self.base_model_class = base_model_class

    def predict(self, image: Image.Image) -> str:
        """
        Use Tesseract OCR to extract text from a PIL Image.
        :param image: PIL Image object.
        :return: Extracted text as a string.
        """
        try:
            # Extract text using pytesseract
            return image_to_string(image)
        except Exception as e:
            raise Exception(f"Error using Tesseract OCR: {str(e)}")
