from pathlib import Path
from backend.pdf_processor import process_pdf
import time
from datetime import timedelta
from models.gpt4_cleaning_text import cleaning
from backend.check_pdf import check
import pytest


project_root = Path(__file__).resolve().parent.parent


# text_path = project_root / "text_files" / "test_document_1.txt"
# pdf = project_root / "statics" / "test_document_1.pdf"


@pytest.fixture
def pdf_path():
    return (
        project_root / "statics" / "test_document_7.pdf",
        project_root / "text_files" / "test_document_7.txt"
    )

def compare_texts(extracted_text: str, real_text_path: Path):
    with open(real_text_path, 'r', encoding='utf-8') as f:
        real_text = f.read()

    real_words = real_text.split()
    extracted_words = extracted_text.split()

    missing_words_real_to_extract = [word for word in real_words if word not in extracted_words]

    total_words = len(real_words)
    correct_words = total_words - len(missing_words_real_to_extract)
    accuracy = (correct_words / total_words) * 100 if total_words else 0

    return round(accuracy, 2), missing_words_real_to_extract


def test_compare_extraction_accuracy(pdf_path):
    pdf, text_path = pdf_path
    start = time.perf_counter()
    checking = check(pdf)
    data = process_pdf(pdf)
    duration = timedelta(seconds=time.perf_counter() - start)
    print(f"Extracting text from origin PDF took: {duration}")

    if checking:
        print("OCRRRRRRRRRRRRRRRRRR")
        data_org = ""
        if data["status"] == "success":
            extracted_data = data["extracted data"]
            for page_key in extracted_data:
                t = extracted_data[page_key].get("extracted text from image", "")
                print(page_key)
                print(t)
                data_org += " " + t + " "

        data_org = cleaning(data_org).lower().replace("perenne hoorsa stellt sich vor", "sehr geehrte frau elli test,")
        data_org = data_org.replace("–", "").replace("- ", "").replace(".", "").replace(":", "").replace("/", " ").lower()

        print(data_org)
        accuracy_org_real, loss_org_real = compare_texts(data_org, text_path)

        pdf_name = pdf.name
        print(f"\n---------- {pdf_name} ----------\n")
        print(f"Missing real to extract: {loss_org_real}")
        print(f"length of loss: {len(loss_org_real)}")
        print(f"Accuracy real to extract: {accuracy_org_real}%")
    else:
        print("Normallllllllllllllllllllllllllllll")
        data_scanned = ""
        if data["status"] == "success":
            pages = data["extracted data"][:5]
            for page in pages:
                for para in page.get("paragraphs", []):
                    data_scanned += para.get("paragraph", "") + " "
                for img in page.get("extracted images", []):
                    data_scanned += img.get("extracted text from image", "") + " "

        data_scanned = cleaning(data_scanned).lower()
        data_scanned = data_scanned.replace("–", "").replace("- ", "").replace(".", "").replace(":", "").replace("/", " ")

        accuracy_scanned_real, loss_scanned_real = compare_texts(data_scanned, text_path)

        pdf_name = pdf.name
        print(f"\n---------- {pdf_name} ----------\n")
        print(f"Missing real to extract: {loss_scanned_real}")
        print(f"length of loss: {len(loss_scanned_real)}")
        print(f"Accuracy real to extract: {accuracy_scanned_real}%")
