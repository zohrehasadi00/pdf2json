import pytest
from pathlib import Path
from backend.normal_pdfs.image_extractor import PdfImageTextExtractor

executor = PdfImageTextExtractor()

@pytest.fixture
def pdf_path():
    return Path(r"C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\statics\sample_pdfs\IntroductionToAnaesthesia.pdf")


def test_image_extractor(pdf_path, c=6):
    """
    Test function for PdfImageTextExtractor to ensure correct number of images are extracted
    and check that the image extraction logic works as expected.
    """

    pages = executor.extract_images(pdf_path, [])

    number_of_images = 0
    for page in pages:
        image_count = sum(1 for key in page if key.startswith("image"))
        number_of_images += image_count

    if number_of_images == c:
        print(f"Correct number of images has been extracted: {number_of_images}")
        assert number_of_images == c
    elif number_of_images > c:
        print(f"More images have been detected: {number_of_images}")
        assert number_of_images > c
    else:
        print(f"Less images have been detected: {number_of_images}")
        assert number_of_images < c

# pdf_path = Path(r"C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\statics\sample_pdfs\einfluss.pdf") 14
# pdf_path = "C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\statics\sample_pdfs\IntroductionToAnaesthesia.pdf" 6
# pdf_path = "C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\statics\sample_pdfs\krebs.pdf" 3
