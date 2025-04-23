import zlib
import base64
import logging
from PIL import Image
from io import BytesIO
from pdf2image import convert_from_bytes


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


def apply_filters(data: bytes, filters: list) -> bytes:
    for f in reversed(filters):
        if f == "/FlateDecode":
            import zlib
            data = zlib.decompress(data)
        elif f == "/LZWDecode":
            data = lzw_decompress(data)
        elif f == "/RunLengthDecode":
            data = run_length_decode(data)
        elif f == "/ASCIIHexDecode":
            data = bytes.fromhex(data.decode("ascii").replace(">", ""))
        elif f == "/ASCII85Decode":
            data = base64.a85decode(data)
        elif f == "/DCTDecode":
            return data
        else:
            logging.warning(f"Unsupported or unhandled filter in sequence: {f}")
            return None
    return data


def decode_image(obj) -> Image.Image | None:
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

        if isinstance(filter_type, list):  # multiple filters
            decoded_data = apply_filters(data, filter_type)
            if decoded_data is None:
                return None
            try:
                return Image.open(BytesIO(decoded_data))

            except Exception:
                try:
                    color_space = obj.get("/ColorSpace", "/DeviceRGB")
                    mode = "RGB" if color_space == "/DeviceRGB" else "L"  # fallback to grayscale
                    expected_length = width * height * (3 if mode == "RGB" else 1)
                    if len(decoded_data) < expected_length:
                        logging.error("Decoded data length mismatch for raw image.")
                        return None
                    return Image.frombytes(mode, (width, height), decoded_data)
                except Exception as e:
                    logging.error(f"Failed to build image from raw data: {str(e)}")
                    return None

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
            decoded_data = lzw_decompress(data)
            return Image.open(BytesIO(decoded_data))

        elif filter_type == "/RunLengthDecode":  # Simple RLE Compression
            try:
                decoded_data = run_length_decode(data)
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
            return None

    except Exception as e:
        logging.error(f"Error decoding image: {str(e)}")
