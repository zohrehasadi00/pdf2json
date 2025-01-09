import pytest
from pathlib import Path
from backend.image_extractor import PdfImageTextExtractor
from PyPDF2 import PdfReader
from PIL import Image
import base64
from io import BytesIO

#TODO: how to get pdfs from example folder??
@pytest.fixture
def sample_pdf():
    """All passed the tests."""
    # return Path("C:/Users/zohre/OneDrive/Desktop/bachelorArbeit/pdf_example/The_Basics_of_Anesthesia_7th_Edition.pdf")    #no pic pdf
    # return Path("C:/Users/zohre/OneDrive/Desktop/bachelorArbeit/pdf_example/IntroductionToAnaesthesia.pdf")  # one with pic
    return Path("C:/Users/zohre/OneDrive/Desktop/bachelorArbeit/pdf_example/test.pdf")


# @pytest.fixture
# def sample_pdf():
#     pdf_path = Path(__file__).parents[2] / 'The_Basics_of_Anesthesia_7th_Edition.pdf'
#     if not pdf_path.exists():
#         raise FileNotFoundError(f"PDF file not found at {pdf_path}")
#     return pdf_path

def test_extract_images(sample_pdf):

    extractor = PdfImageTextExtractor()
    reader = PdfReader(sample_pdf)

    for page_number, page in enumerate(reader.pages, start=1):
        print(f"Processing Page {page_number}...")
        images = extractor.extract_images(page)

        for image_data in images:
            base64_image = image_data["Base64Image"]
            extracted_text = image_data["ExtractedText"]
            assert isinstance(base64_image, str), "Base64Image is not a string."
            assert base64_image.strip() != "", "Base64Image is an empty string."

            try:
                image_bytes = BytesIO(base64.b64decode(base64_image))
                image = Image.open(image_bytes)
                image.verify()
            except Exception as e:
                pytest.fail(f"Decoded image is invalid: {str(e)}")

            assert isinstance(extracted_text, str), "Extracted text is not a string."
            print(f"Page {page_number}, Extracted Text: {extracted_text}")


def test_extract_text_from_image():

    extractor = PdfImageTextExtractor()
    image = Image.new("RGB", (100, 50), color="white")
    extracted_text = extractor.extract_text_from_image(image)
    assert isinstance(extracted_text, str), "Extracted text is not a string."
    print(f"Extracted Text from Image: {extracted_text}")


def test_image_to_base64():
    extractor = PdfImageTextExtractor()
    image = Image.new("RGB", (100, 50), color="blue")
    base64_image = extractor.image_to_base64(image)
    assert isinstance(base64_image, str), "Base64 result is not a string."
    assert base64_image.strip() != "", "Base64 result is an empty string."
    try:
        image_bytes = BytesIO(base64.b64decode(base64_image))
        decoded_image = Image.open(image_bytes)
        decoded_image.verify()
    except Exception as e:
        pytest.fail(f"Decoded image from base64 is invalid: {str(e)}")

    print("Image successfully encoded and decoded as Base64.")


def test_combined_processing(sample_pdf):
    extractor = PdfImageTextExtractor()
    reader = PdfReader(sample_pdf)

    for page_number, page in enumerate(reader.pages, start=1):
        print(f"Processing Page {page_number}...")
        try:
            images = extractor.extract_images(page)
            for image_data in images:
                base64_image = image_data["Base64Image"]
                extracted_text = image_data["ExtractedText"]
                assert isinstance(base64_image, str), "Base64Image is not a string."
                assert base64_image.strip() != "", "Base64Image is an empty string."
                assert isinstance(extracted_text, str), "ExtractedText is not a string."
                print(f"Page {page_number}, Base64Image Length: {len(base64_image)}, Extracted Text: {extracted_text}")

        except Exception as e:
            pytest.fail(f"Error during combined processing of page {page_number}: {str(e)}")


def test_extract_images_page_3(sample_pdf):
    extractor = PdfImageTextExtractor()
    reader = PdfReader(sample_pdf)
    if len(reader.pages) < 3:
        print(f"Warning: The PDF only has {len(reader.pages)} pages. Skipping image extraction for page 3.")
        return
    page_3 = reader.pages[2]
    print("Processing Page 3...")
    images = extractor.extract_images(page_3)
    for image_data in images:
        base64_image = image_data["Base64Image"]
        extracted_text = image_data["ExtractedText"]
        assert isinstance(base64_image, str), "Base64Image is not a string."
        assert base64_image.strip() != "", "Base64Image is an empty string."
        try:
            image_bytes = BytesIO(base64.b64decode(base64_image))
            image = Image.open(image_bytes)
            image.verify()
        except Exception as e:
            pytest.fail(f"Decoded image is invalid: {str(e)}")
        assert isinstance(extracted_text, str), "Extracted text is not a string."
        print(f"Page 3, Base64Image Length: {len(base64_image)}, Extracted Text: {extracted_text}")
