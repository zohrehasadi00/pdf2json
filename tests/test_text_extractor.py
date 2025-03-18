import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pdfplumber
from collections import Counter
import re


def extract_text_from_pdf(pdf_path):
    extracted_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text() + " "
    return extracted_text.strip()


def evaluate_text_extraction(raw_text, extracted_text):
    def normalize(text):
        return re.sub(r'[^\w\s]', '', text.lower()).split()

    raw_words = normalize(raw_text)
    extracted_words = normalize(extracted_text)

    raw_count = Counter(raw_words)
    extracted_count = Counter(extracted_words)

    correct_count = sum(min(raw_count[word], extracted_count[word]) for word in raw_count)

    if not raw_words:
        return 100.0, 0.0, 0

    total_words = len(raw_words)
    accuracy = (correct_count / total_words) * 100
    loss_percent = 100 - accuracy
    lost_words = total_words - correct_count

    return accuracy, loss_percent, lost_words


def test_pdf_text_extraction():
    # pdf_path = r"C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\statics\sample_pdfs\IntroductionToAnaesthesia.pdf"  # Change this to your test PDF file path
    # raw_text_path = r"C:\\Users\\zohre\\OneDrive\\Desktop\\bachelorArbeit\\statics\\sample_pdfs\\extracted_text.txt"

    # pdf_path = r"C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\statics\sample_pdfs\krebs.pdf"
    # raw_text_path = r"C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\statics\sample_pdfs\krebs.txt"

    pdf_path = r"C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\statics\sample_pdfs\einfluss.pdf"
    raw_text_path = r"C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\statics\sample_pdfs\einfluss.txt"

    with open(raw_text_path, "r", encoding="utf-8") as file:
        raw_text = file.read().strip()

    extracted_text = extract_text_from_pdf(pdf_path)
    accuracy, loss_percent, lost_words = evaluate_text_extraction(raw_text, extracted_text)
    print("\n")
    print(f"Accuracy: {accuracy:.2f}%\n")
    print(f"Loss: {loss_percent:.2f}% ({lost_words} words)")

