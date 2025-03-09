import base64
import PyPDF2
import logging
import json
import time
from PIL import Image
from typing import List, Dict
from io import BytesIO
from pathlib import Path
from models.tesseract_ocr_model import TesseractOcrModel
from models.base_ocr_model import BaseOcrModel
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from models.blip_model import BlipModel
from datetime import timedelta

blip = BlipModel()


class PdfImageTextExtractor:
    def __init__(self):
        self.ocr_model = TesseractOcrModel(BaseOcrModel)
        self.sentence_model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight embedding model

    def _decode_image(self, obj) -> Image.Image:
        """
        Decodes a PDF image object into a PIL Image.

        Args:
            obj: The PDF image object.

        Returns:
            Image.Image: The decoded image or None if decoding fails.
        """
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

        return None

    def extract_images(self, file_path: Path, page_data: List[dict]) -> List[Dict]:
        """
        Extracts images and associated text from the provided PDF file.
        Args:
            file_path (Path): The file path to the PDF document.
            page_data (List[dict]): List of all paragraphs from pages
        Returns:
            List[Dict]: A list of dictionaries, each representing a page with grouped images.
        """
        logging.info("Start processing images and the data of the pdf")
        start_time = time.perf_counter()
        pages = []
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                logging.info("pdf has been read")
                for page_number, page in enumerate(reader.pages, 1):
                    # pdftext = page.extract_text()
                    resources = page.get("/Resources")
                    if not resources or "/XObject" not in resources:
                        continue
                    xObject = resources["/XObject"].get_object()
                    page_images = {}
                    image_count = 1
                    for obj_name in xObject:
                        obj = xObject[obj_name]
                        if obj.get("/Subtype") == "/Image":
                            image = self._decode_image(obj)
                            if image is None:
                                logging.warning(f"Skipping a failed image on page {page_number}.")
                                continue
                            logging.info("processing image64")
                            base64_image = self.image_to_base64(image)
                            logging.info("processing description")
                            description = self.describe(base64_image)
                            logging.info("extracting text from image")
                            extracted_text = self.extract_text_from_image(image)
                            logging.info("and matching")
                            match = self.visualLink(image, page_data, page_number)
                            page_images[f"image{image_count}"] = {
                                "Base64 of Image": base64_image,
                                "Image Description": description,
                                "Extracted Text From Image": extracted_text,
                                "Related paragraph/s": match
                            }
                            image_count += 1
                    if page_images:
                        pages.append({
                            "Page": f"Page {page_number}",
                            **page_images  # Add the images as individual keys
                        })
            duration = timedelta(seconds=time.perf_counter() - start_time)
            logging.info(f"Summarization took: {duration}")

        except Exception as e:
            logging.error(f"Error extracting images from PDF {file_path}: {str(e)}")
        return pages

    def extract_text_from_image(self, image: Image.Image) -> str:
        """
        Extracts text from an image using OCR.

        Args:
            image (Image.Image): The PIL Image object.

        Returns:
            str: The extracted text, or an empty string on failure.
        """
        try:
            text = self.ocr_model.predict(image)
            text = text.replace("\n\n", "__")
            text = text.replace("\n", "")
            text = text.replace("%) Thieme Compliance", "No text found")
            return text
        except Exception as e:
            logging.error(f"Error extracting text from image: {str(e)}")
            return ""

    @staticmethod
    def image_to_base64(image: Image.Image) -> str:
        """
        Converts a PIL Image to a Base64-encoded string.

        Args:
            image (Image.Image): The PIL Image object.

        Returns:
            str: The Base64-encoded string, or an empty string on failure.
        """
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

    def visualLink(self, image: Image.Image, page_data: List[dict], page_number: int) -> str:
        """
        This function will receive a decoded image (Pillow Image object), the page data,
        and the page number. It will search through paragraphs on the given page and
        return the most relevant paragraph or 'No related paragraph found'.

        Args:
            image (Image.Image): Decoded image.
            page_data (List[dict]): List of paragraphs for the page.
            page_number (int): The page number to filter paragraphs.

        Returns:
            str: The most relevant paragraph related to the image, or 'No related paragraph found'.
        """
        extracted_text = self.extract_text_from_image(image)
        relevant_paragraphs = [para for para in page_data if para.get('page') == page_number]

        for paragraph in relevant_paragraphs:
            paragraph_text = paragraph["paragraph"]
            if extracted_text.lower() in paragraph_text.lower():
                return paragraph_text

        return "No related paragraph found"

    def describe(self, base64_image: str) -> str:
        """
        Generates a description for the given image using the BLIP model.

        Args:
            base64_image: String from image_to_base64 function

        Returns:
            str: The image description generated by the model.
        """
        try:
            caption = blip.generate_caption(base64_image)
            return caption
        except Exception as e:
            logging.error(f"Error generating image description: {str(e)}")
            return "Error generating description."
