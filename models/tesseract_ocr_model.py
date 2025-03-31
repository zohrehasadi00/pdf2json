from PIL import Image
from pytesseract import image_to_string
from models.base_ocr_model import BaseOcrModel


class TesseractOcrModel(BaseOcrModel):
    """Implementation of the OCR model using Tesseract."""

    def __init__(self, base_model_class):
        if not issubclass(base_model_class, BaseOcrModel):
            raise ValueError("Base model must inherit from BaseOcrModel.")
        self.base_model_class = base_model_class

        self.settings = None or {
            'language': 'eng+deu',   # Extract and finding both English and German words
            'psm': 3,  # Page segmentation mode
            'oem': 3,  # OCR engine mode
        }

    def predict(self, image: Image.Image) -> str:
        """
        Use Tesseract OCR to extract text from a PIL Image.
        :param image: PIL Image object.
        :return: Extracted text as a string.
        """
        try:
            custom_config = f'--psm {self.settings["psm"]} --oem {self.settings["oem"]}'
            return image_to_string(image, lang=self.settings['language'], config=custom_config)

        except Exception as e:
            raise Exception(f"Error using Tesseract OCR: {str(e)}")



