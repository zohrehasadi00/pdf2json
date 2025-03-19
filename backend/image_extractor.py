import base64
import PyPDF2
import logging
from PIL import Image
from typing import List, Dict
from io import BytesIO
from pathlib import Path
from models.tesseract_ocr_model import TesseractOcrModel
from models.base_ocr_model import BaseOcrModel
from sentence_transformers import SentenceTransformer
from models.blip_model import BlipModel
from pdf2image import convert_from_bytes

# from datetime import timedelta
# import time


blip = BlipModel()


class PdfImageTextExtractor:
    def __init__(self):
        self.ocr_model = TesseractOcrModel(BaseOcrModel)
        self.sentence_model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight embedding model

    @staticmethod
    def lzw_decompress(data: bytes) -> bytes:
        """
        Decompresses LZW-encoded data from PDFs.

        Args:
            data (bytes): LZW compressed data.

        Returns:
            bytes: Decompressed data.
        """
        try:
            import lzma
            decompressed_data = lzma.decompress(data)
            return decompressed_data
        except ImportError:
            logging.error("LZW decompression failed: 'lzma' library not found.")
            return b""

    @staticmethod
    def run_length_decode(data: bytes) -> bytes:
        """
        Decodes Run-Length encoded data from PDFs.

        Args:
            data (bytes): Run-Length compressed data.

        Returns:
            bytes: Decompressed data.
        """
        output = bytearray()
        i = 0
        while i < len(data):
            length = data[i]
            i += 1
            if length < 128:
                output.extend(data[i:i + length + 1])
                i += length + 1
            elif length > 128:
                output.extend(data[i:i + 1] * (257 - length))
                i += 1
            elif length == 128:
                break
        return bytes(output)

    @staticmethod
    def _decode_image(obj) -> Image.Image | None:
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

            if "/Filter" not in obj:
                logging.warning("No filter found for the image.")
                return None

            filter_type = obj["/Filter"]

            if filter_type == "/DCTDecode":  # JPEG
                return Image.open(BytesIO(data))
            elif filter_type == "/JPXDecode":  # JPEG 2000
                return Image.open(BytesIO(data))
            elif filter_type == "/FlateDecode":  # PNG-like
                color_space = obj.get("/ColorSpace", "/DeviceRGB")
                mode = "RGB" if color_space == "/DeviceRGB" else "P"
                return Image.frombytes(mode, (width, height), data)

            elif filter_type == "/CCITTFaxDecode":  # Fax (1-bit TIFF)

                return Image.frombytes("1", (width, height), data)

            elif filter_type == "/LZWDecode":  # LZW (TIFF compression)

                decoded_data = PdfImageTextExtractor.lzw_decompress(data)

                return Image.open(BytesIO(decoded_data))
            elif filter_type == "/RunLengthDecode":  # Simple RLE Compression
                try:
                    decoded_data = PdfImageTextExtractor.run_length_decode(data)
                    return Image.open(BytesIO(decoded_data))
                except Exception as e:
                    logging.error(f"RunLengthDecode failed: {str(e)}")
            elif filter_type == "/ASCIIHexDecode":  # ASCII Hex Encoding
                try:
                    decoded_data = bytes.fromhex(data.decode("ascii").replace(">", ""))
                    return Image.open(BytesIO(decoded_data))
                except Exception as e:
                    logging.error(f"ASCIIHexDecode failed: {str(e)}")
            elif filter_type == "/ASCII85Decode":  # ASCII85 Encoding
                try:
                    decoded_data = base64.a85decode(data)
                    return Image.open(BytesIO(decoded_data))
                except Exception as e:
                    logging.error(f"ASCII85Decode failed: {str(e)}")
            elif filter_type == "/JBIG2Decode":  # JBIG2 Compression
                logging.warning("JBIG2 decoding requires an external decoder.")
                try:
                    images = convert_from_bytes(data)
                    return images[0] if images else None
                except Exception as e:
                    logging.error(f"JBIG2 decoding failed: {str(e)}")
                    return None
            elif filter_type == "/Crypt":
                logging.warning("Encrypted image detected. Cannot decode without decryption.")
                return None
            else:
                logging.warning(f"Unsupported image filter: {filter_type}")

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
        # logging.info("Start processing images and the data of the pdf")
        # start_time = time.perf_counter()
        pages = []
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                # logging.info("pdf has been read")
                for page_number, page in enumerate(reader.pages, 1):
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

                            base64_image = self.image_to_base64(image)
                            extracted_text = self.extract_text_from_image(image)
                            match = self.visualLink(image, page_data, page_number)
                            page_images[f"image{image_count}"] = {
                                "base64 of image": base64_image,
                                "extracted text from image": extracted_text,
                                "related paragraph/s": match
                            }
                            image_count += 1
                    if page_images:
                        pages.append({
                            "page": f"page {page_number}",
                            **page_images  # Add the images as individual keys
                        })
            # duration = timedelta(seconds=time.perf_counter() - start_time)
            # logging.info(f"Summarization took: {duration}")

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
        extracted_text = self.extract_text_from_image(image)

        page_entry = next((entry for entry in page_data if entry.get("page") == page_number), None)

        if not page_entry or "data" not in page_entry or "paragraphs" not in page_entry["data"]:
            return "No related paragraph found"

        relevant_paragraphs = page_entry["data"]["paragraphs"]

        for paragraph in relevant_paragraphs:
            paragraph_text = paragraph["paragraph"]
            if extracted_text.lower() in paragraph_text.lower():
                return paragraph_text

        return "No related paragraph found"
