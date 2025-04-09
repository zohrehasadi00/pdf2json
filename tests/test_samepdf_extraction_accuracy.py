from pathlib import Path
from backend.pdf_processor import process_pdf
import time
from datetime import timedelta
from models.gpt4_cleaning_text import cleaning

# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Aßußfere Wendung.txt")
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Aßußfere Wendung.pdf")

# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Geburtseinleitung.txt")
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Geburtseinleitung .pdf")

# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Geburtshilf.txt") #problematik
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Geburtshilfe.pdf")

# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\test.txt")
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\test.pdf")

# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Kaiserschnitt.txt")
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Kaiserschnitt.pdf")

# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Narkose.txt")
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Narkose.pdf")

# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Geburtshilfliche Maßnahmen.txt")
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Geburtshilfliche Maßnahmen.pdf")

text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Geburtshilfliche_nahmen.txt")
pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Geburtshilfliche_nahmen.pdf")

# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\IntroductionToAnaesthesia.txt")
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\IntroductionToAnaesthesia.pdf")

# text_path = Path()
# pdf = Path()

# text_path = Path()
# pdf = Path()

# text_path = Path()
# pdf = Path()

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



def test_compare_extraction_accuracy():
#     start = time.perf_counter()
#     data = process_pdf(pdf)
#
#     duration2 = timedelta(seconds=time.perf_counter() - start)
#     print(f"\nExtracting text from scanned PDF took: {duration2}")
#
#     data_scanned = ""
#     if data["status"] == "success":
#         pages = data["extracted data"][:5]  # Only pages 1 to 8 (index 0–7)
#         for page in pages:
#             for para in page.get("paragraphs", []):
#                 data_scanned += para.get("paragraph", "") + " "
#             # for img in page.get("extracted images", []):
#             #     data_scanned += img.get("extracted text from image", "") + " "
#
#     data_scanned = cleaning(data_scanned).lower()
#     # print(data_scanned)
#     accuracy_scanned_real, loss_scanned_real = compare_texts(data_scanned, text_path)
#
#     # _____________________
#     pdf_name = pdf.name
#     print(f"\n---------- {pdf_name} ----------\n")
#     print(f"Missing real to extract: {loss_scanned_real}")
#     print(f"length of loss: {len(loss_scanned_real)}")
#     print(f"Accuracy real to extract: {accuracy_scanned_real}%")
# _____________________________________


    start1 = time.perf_counter()
    data1 = process_pdf(pdf)
    duration1 = timedelta(seconds=time.perf_counter() - start1)
    print(f"Extracting text from origin PDF took: {duration1}")

    data_org = ""
    if data1["status"] == "success":
        extracted_data = data1["extracted data"]
        for page_key in extracted_data:  # Iterate through all pages
            data_org += " " + extracted_data[page_key].get("extracted text from image", "") + " "


    data_org = cleaning(data_org).lower()
    print(data_org)
    accuracy_org_real, loss_org_real = compare_texts(data_org, text_path)
# _____________________
    pdf_name = pdf.name
    print(f"\n---------- {pdf_name} ----------\n")
    print(f"Missing real to extract: {loss_org_real}")
    print(f"length of loss: {len(loss_org_real)}")
    print(f"Accuracy real to extract: {accuracy_org_real}%")
