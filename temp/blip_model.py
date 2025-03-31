import base64
import logging
from io import BytesIO
from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor
import torch


class BlipModel:
    def __init__(self, model_name: str = "Salesforce/blip-image-captioning-base", device: str = None):
        """
        Initializes the BLIP model and processor.

        Args:
            model_name (str): The name of the BLIP model to use.
            device (str): The device to run the model on ('cuda' or 'cpu').
                          If None, it defaults to GPU if available.
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name).to(self.device)

    def generate_caption(self, image_base64: str) -> str:
        """
        Generate a caption for the provided base64-encoded image.

        Args:
            image_base64 (str): Base64 string of the image.

        Returns:
            str: The generated caption or an error message on failure.
        """
        try:
            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data)).convert("RGB")

            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            output = self.model.generate(**inputs)
            return self.processor.decode(output[0], skip_special_tokens=True)

        except Exception as e:
            logging.error(f"Error generating caption: {str(e)}")
            return "Error generating caption."
