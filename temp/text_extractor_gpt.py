import json
import logging
from typing import Dict, List
from temp.gpt4_sections import detect_sections
import pdfplumber
from pathlib import Path
from models.gpt4_summary import summarize_text

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_text_and_summarize(file_path: Path, preview_first_page: bool = False) -> List[Dict]:
    """Extracts text from each page and processes it with section detection.

    Args:
        file_path: Path to the PDF file
        preview_first_page: If True, only processes the first page for quick testing
    """
    page_data = []

    with pdfplumber.open(file_path) as pdf:
        # Get either just the first page or all pages based on flag
        pages_to_process = [pdf.pages[0]] if preview_first_page else pdf.pages

        for page in pages_to_process:
            try:
                text = page.extract_text() or ""
                sections = []

                if text.strip():
                    try:
                        detected_sections = detect_sections(text.strip()) or []

                        for section in detected_sections:
                            if isinstance(section, dict):
                                section_title = section.get('section_title') or section.get(
                                    'section') or "Untitled Section"
                                content = section.get('content', '')

                                summary = ""
                                if content:
                                    try:
                                        summary = summarize_text(content)
                                    except Exception as e:
                                        logging.warning(f"Summary failed for section: {str(e)}")
                                        summary = "Summary unavailable"

                                sections.append({
                                    "section_title": section_title,
                                    "content": content,
                                    "summary": summary
                                })
                    except Exception as e:
                        logging.error(f"Section detection failed: {str(e)}")
                        sections.append({
                            "section_title": "Processing Error",
                            "content": text.strip(),
                            "summary": "Section detection failed"
                        })

                page_data.append({
                    "page": page.page_number,
                    "sections": sections
                })

            except Exception as e:
                logging.error(f"Page {page.page_number} error: {str(e)}")
                page_data.append({
                    "page": page.page_number,
                    "sections": [{
                        "section_title": "Error",
                        "content": "Page processing failed",
                        "summary": "No summary available"
                    }]
                })

    return page_data


if __name__ == "__main__":
    file = Path(r"C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\statics\sample_pdfs\krebs.pdf")


    PREVIEW_MODE = True

    try:
        result = extract_text_and_summarize(file, preview_first_page=PREVIEW_MODE)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        logging.error(f"Failed to process PDF: {str(e)}")
        print(json.dumps([{"error": str(e)}], indent=2))