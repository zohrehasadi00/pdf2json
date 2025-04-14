import base64
import logging
from PIL import Image
from io import BytesIO


def image_to_base64(image: Image.Image) -> str:
    """
    Converts a PIL Image to a Base64-encoded string.

    Args:
        image (Image.Image): The PIL Image object.

    Returns:
        str: The Base64-encoded string, or an empty string on failure.
    """
    try:
        logging.info("Converting image to base64")
        if image.mode == "CMYK":
            image = image.convert("RGB")

        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode("utf-8")

    except Exception as e:
        logging.error(f"Error encoding image to base64: {str(e)}")
        return ""
