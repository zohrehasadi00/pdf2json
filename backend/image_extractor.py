import os
import json
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from PIL import Image
from typing import List, Dict
import base64
from io import BytesIO
import logging
from pathlib import Path
from models.tesseract_ocr_model import TesseractOcrModel
from models.base_ocr_model import BaseOcrModel
import PyPDF2
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from models.blip_model import BlipModel
import pdfplumber

blip = BlipModel()


class PdfImageTextExtractor:
    def __init__(self):
        self.ocr_model = TesseractOcrModel(BaseOcrModel)
        self.sentence_model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight embedding model

    @staticmethod
    def _decode_image(obj) -> Image.Image:
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

    def extract_images(self, file_path: Path) -> List[Dict]:
        """
        Extracts images and associated text from the provided PDF file.

        Args:
            file_path (Path): The file path to the PDF document.

        Returns:
            List[Dict]: A list of dictionaries, each representing a page with grouped images.
        """
        pages = []
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)

                for page_number, page in enumerate(reader.pages, 1):
                    pdftext = ""
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

                            # Process the image
                            base64_image = self.image_to_base64(image)
                            match = self.visualLink(pdftext, base64_image)
                            extracted_text = self.extract_text_from_image(image)

                            # Store the image and its data under keys like image1, image2, etc.
                            page_images[f"image{image_count}"] = {
                                "Base64Image": base64_image,
                                "ExtractedText": extracted_text,
                                "Related paragraph/s": match
                            }
                            image_count += 1

                    if page_images:
                        pages.append({
                            "Page": f"Page {page_number}",
                            **page_images  # Add the images as individual keys
                        })

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
            #if image.mode == "CMYK":
            #    image = image.convert("RGB")
#
            #buffer = BytesIO()
            #image.save(buffer, format="PNG")
            #buffer.seek(0)
            #return base64.b64encode(buffer.read()).decode("utf-8")
            return "this is 64"
        except Exception as e:
            logging.error(f"Error converting image to base64: {str(e)}")
            return ""

    def visualLink(self, text: str, code: str) -> str:
        """
            Match image base64 to the most relevant paragraph based on the image caption and paragraph text using BLIP model that it calls

            Args:
            - extracted text from the page
            - images_base64 of the image

            Returns:
            - the related paragraph from the given text to the image.
            """
        try:
            paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
            if not paragraphs:
                return "No relevant text found."

            paragraph_embeddings = self.sentence_model.encode(paragraphs)
            caption = blip.generate_caption(code)
            caption_embedding = self.sentence_model.encode([caption])
            similarities = cosine_similarity(caption_embedding, paragraph_embeddings)

            most_similar_index = similarities.argmax()
            most_similar_paragraph = paragraphs[most_similar_index]

            most_similar_score = similarities[0][most_similar_index]
            similarity_threshold = 0.2
            if most_similar_score < similarity_threshold:
                return "No related paragraph was found"

            return most_similar_paragraph
        except Exception as e:
            logging.error(f"Error in visualLink: {str(e)}")
            return "Error finding related text."

#x = PdfImageTextExtractor()
#res = x.extract_images(file_path=Path(r"C:\Users\zohre\bachelorT\MediLink\example\sample_pdfs\IntroductionToAnaesthesia.pdf"))
#print(json.dumps(res, indent=4))