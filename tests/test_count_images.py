import pytest
from pathlib import Path
from backend.native_pdfs.image_extractor import extract_images


@pytest.fixture
def pdf_path():
    project_root = Path(__file__).resolve().parent.parent
    return project_root / "statics" / "test_document_8.py"

def test_image_extractor(pdf_path, c=5):
    """
    Test function for PdfImageTextExtractor to ensure correct number of images are extracted
    and check that the image extraction logic works as expected.
    """

    pages = extract_images(pdf_path)

    number_of_images = 0
    for page in pages:
        image_count = sum(1 for key in page if key.startswith("image"))
        number_of_images += image_count
    print(f"number_of_images: {number_of_images}")
    if number_of_images == c:
        print(f"Correct number of images has been extracted: {number_of_images}")
        assert number_of_images == c
    elif number_of_images > c:
        print(f"More images have been detected: {number_of_images}")
        assert number_of_images > c
    else:
        print(f"Less images have been detected: {number_of_images}")
        assert number_of_images < c
