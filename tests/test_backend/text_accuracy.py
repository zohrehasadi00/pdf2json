from difflib import SequenceMatcher
import pdfplumber
from pathlib import Path
from typing import List


def extract_text(file_path: Path) -> str:
    result = []

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    with pdfplumber.open(file_path) as pdf:
        if not pdf.pages:
            raise ValueError(f"The PDF file '{file_path}' has no pages.")

        page = pdf.pages[0]
        try:
            text = page.extract_text()
            if text:
                result.append(text)
        except Exception as page_error:
            print(page_error)

    return "\n".join(result)


def calculate_accuracy(real_text: str, extracted_text: str) -> float:
    similarity_ratio = SequenceMatcher(None, real_text, extracted_text).ratio()
    return similarity_ratio * 100


def load_real_text() -> str:
    script_dir = Path(__file__).parent
    real_text_path = script_dir / "real_text.txt"

    if not real_text_path.exists() or not real_text_path.is_file():
        raise FileNotFoundError(f"Real text file not found: {real_text_path}")

    with open(real_text_path, "r", encoding="utf-8") as file:
        return file.read()


pdf_path = Path(r"C:/Users/zohre/OneDrive/Desktop/bachelorArbeit/pdf_example/The_Basics_of_Anesthesia_7th_Edition.pdf")

try:
    real_text = load_real_text()
    extracted_text = extract_text(pdf_path)
    accuracy = calculate_accuracy(real_text, extracted_text)
    print(f"Accuracy of extracted text: {accuracy:.2f}%")
except Exception as e:
    print(f"Error: {e}")
