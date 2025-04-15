class BaseOcrModel:
    """Base class for OCR models: Future plan; useful when multiple engines exist"""

    def predict(self, image):
        """
        Abstract method for text prediction.
        :param image: PIL Image to extract text from.
        :return: Extracted text as a string.
        """
        pass
