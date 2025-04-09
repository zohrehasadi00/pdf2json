import json
from pathlib import Path
import pdfplumber
from backend.native_pdfs.text_extractor import extract_text_and_summarize


def test_text():
    try:
        pdf_path = Path(r"C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\statics\sample_pdfs\IntroductionToAnaesthesia.pdf")
        with pdfplumber.open(pdf_path) as pdf:
            page_data = []
            for page in pdf.pages:
                info = {"page": page.page_number, "data": extract_text_and_summarize(page)}
                page_data.append(info)

    except Exception as e:
        print(e)


    print(json.dumps(page_data, indent=4))
