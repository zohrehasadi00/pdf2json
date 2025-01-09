from PIL import Image
from typing import List, Dict
import base64
from io import BytesIO
import logging
from models.tesseract_ocr_model import TesseractOcrModel
from models.base_ocr_model import BaseOcrModel


class PdfImageTextExtractor:
    def __init__(self):
        self.ocr_model = TesseractOcrModel(BaseOcrModel)

    @staticmethod
    def _decode_image(obj) -> Image.Image:
        try:
            data = obj._data  # noqa: Access to protected member '_data'
            width, height = obj["/Width"], obj["/Height"]

            if "/Filter" in obj:
                filter_type = obj["/Filter"]
                if filter_type == "/DCTDecode":
                    return Image.open(BytesIO(data))
                elif filter_type == "/JPXDecode":
                    return Image.open(BytesIO(data))
                elif filter_type == "/FlateDecode":
                    color_space = obj.get("/ColorSpace", "/DeviceRGB")
                    mode = "RGB" if color_space == "/DeviceRGB" else "P"
                    return Image.frombytes(mode, (width, height), data)
                else:
                    logging.warning(f"Unsupported image filter: {filter_type}")
            else:
                logging.warning("No filter found for the image.")
        except Exception as e:
            logging.error(f"Error decoding image: {str(e)}")

    def extract_images(self, page) -> List[Dict]:
        images = []
        try:
            resources = page["/Resources"]
            if "/XObject" not in resources:
                logging.warning("No images found on this page.")
                return images

            xObject = resources["/XObject"].get_object()

            for obj_name in xObject:
                obj = xObject[obj_name]
                if obj["/Subtype"] == "/Image":
                    image = self._decode_image(obj)
                    if image is None:
                        logging.warning("Skipping a failed image.")
                        continue

                    base64_image = self.image_to_base64(image)
                    extracted_text = self.ocr_model.predict(image)

                    images.append({
                        "Base64Image": base64_image,
                        "ExtractedText": extracted_text
                    })
        except Exception as e:
            logging.error(f"Error extracting images: {str(e)}")
        return images

    def extract_text_from_image(self, image: Image.Image) -> str:
        try:
            text = self.ocr_model.predict(image)
            return text
        except Exception as e:
            logging.error(f"Error extracting text from image: {str(e)}")
            return ""

    @staticmethod
    def image_to_base64(image: Image.Image) -> str:
        try:
            if image.mode == "CMYK":
                image = image.convert("RGB")

            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
            return base64.b64encode(buffer.read()).decode("utf-8")
        except Exception as e:
            logging.error(f"Error converting image to base64: {str(e)}")
            return ""
