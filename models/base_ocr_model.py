class BaseOcrModel:
    """Base class for OCR models."""

    def predict(self, image):
        """
        Abstract method for text prediction.
        :param image: PIL Image to extract text from.
        :return: Extracted text as a string.
        """
        raise NotImplementedError("Subclasses must implement the `predict` method.")
