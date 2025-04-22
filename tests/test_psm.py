import json
import io
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
import fitz  # PyMuPDF
import pytest
from pathlib import Path
import time
import logging
from datetime import timedelta
from backend.imgRelated.text_from_img import extract_text_from_image
from models.gpt4_cleaning_text import cleaning

# Test file pairs (uncomment the pair you want to test)
test_cases = [
      #(Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Aßußfere Wendung.txt"),
      # Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Aßußfere Wendung.pdf")),

    # (Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Geburtseinleitung.txt"),
    #  Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Geburtseinleitung .pdf")),

    # (Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Geburtshilf.txt"),
    #  Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Geburtshilfe.pdf")),

     (Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\test.txt"),
      Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\test.pdf")),

    # (Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Kaiserschnitt.txt"),
    #  Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Kaiserschnitt.pdf")),

    # (Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Narkose.txt"),
    #  Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Narkose.pdf")),

    # (Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Geburtshilfliche Maßnahmen.txt"),
    #  Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Geburtshilfliche Maßnahmen.pdf")),

     # (Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Geburtshilfliche_nahmen - edited.txt"),
     # Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Geburtshilfliche_nahmen.pdf"))
    ]


def convert_pdf_to_images(pdf_path: Path) -> list[tuple[int, Image.Image]]:
    """Convert PDF pages to PIL Images with page numbers."""
    images = []
    try:
        with fitz.open(pdf_path) as pdf_document:
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                images.append((page_num + 1, img))
    except Exception as e:
        logging.error(f"Failed to process PDF {pdf_path}: {str(e)}")
        raise
    return images


def process_single_page(args: tuple[int, Image.Image]) -> tuple[int, str] | None:
    """Process a single page image to extract text."""
    page_number, image = args
    try:
        start_time = time.perf_counter()
        extracted_text = extract_text_from_image(image)
        duration = timedelta(seconds=time.perf_counter() - start_time)
        print(duration)
        return (page_number, extracted_text)
    except Exception as e:
        logging.warning(f"Failed to process page {page_number}: {str(e)}")
        return None


def combine_ocr_text(ocr_data: list[tuple[int, str]]) -> str:
    """Combine OCR results into a single normalized text string."""
    ocr_data.sort(key=lambda x: x[0])
    combined = " ".join(text for _, text in ocr_data if text.strip())
    combined = cleaning(combined).replace("–", "").replace("- ", "").replace(".", "").replace(":", "").replace("/", " ").lower().replace("\n", " ").replace("  ", " ").strip()
    print(combined)
    return combined


def calculate_accuracy(ground_truth: str, ocr_text: str) -> tuple[float, list[str]]:
    """Calculate word-level accuracy between ground truth and OCR text."""
    truth_words = ground_truth.lower().split()
    ocr_words = ocr_text.split()

    missing_words = [word for word in truth_words if word not in ocr_words]
    accuracy = (len(truth_words) - len(missing_words)) / len(truth_words) * 100 if truth_words else 0

    return round(accuracy, 2), missing_words


@pytest.fixture(params=test_cases)
def test_case(request):
    """Pytest fixture providing test case pairs"""
    text_path, pdf_path = request.param
    with open(text_path, 'r', encoding='utf-8') as f:
        return f.read(), pdf_path


def test_ocr_accuracy(test_case):
    """Test OCR accuracy against ground truth text"""
    ground_truth, pdf_path = test_case

    # Process PDF
    image_pages = convert_pdf_to_images(pdf_path)
    ocr_results = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_single_page, (page_num, img))
                   for page_num, img in image_pages]

        for future in as_completed(futures):
            if (result := future.result()):
                ocr_results.append(result)

    # Analyze results
    combined_ocr = combine_ocr_text(ocr_results)
    accuracy, missing_words = calculate_accuracy(ground_truth, combined_ocr)

    print(f"\nOCR Accuracy: {accuracy}%")
    print(f"Missing words: {missing_words[:20]}")  # Print first 20 missing words

    # Save results for inspection
    results = {
        "accuracy": accuracy,
        "missing_words_count": len(missing_words),
        "sample_missing_words": missing_words[:20],
        "ocr_text": combined_ocr[:1000] + "..." if len(combined_ocr) > 1000 else combined_ocr
    }

    with open("ocr_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    assert accuracy > 50.0  # Minimum acceptable accuracy threshold


if __name__ == "__main__":
    # For manual testing without pytest
    text_path, pdf_path = test_cases[-1]  # Use last test case

    with open(text_path, 'r', encoding='utf-8') as f:
        ground_truth = f.read()

    image_pages = convert_pdf_to_images(pdf_path)
    ocr_results = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_single_page, (page_num, img))
                   for page_num, img in image_pages]

        for future in as_completed(futures):
            if (result := future.result()):
                ocr_results.append(result)

    combined_ocr = combine_ocr_text(ocr_results)
    accuracy, missing_words = calculate_accuracy(ground_truth, combined_ocr)

    print(f"\nFinal OCR Accuracy: {accuracy}%")
    print(f"Total missing words: {len(missing_words)}")
    print(f"Sample missing words: {missing_words[:20]}")