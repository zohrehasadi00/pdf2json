import logging
from typing import Dict
from models.gpt4 import summarize_text
# import time
# from datetime import timedelta

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_text_and_summarize(page) -> Dict:
    # start_time = time.perf_counter()
    try:
        # time.sleep(1)
        text = page.extract_text()
        text = text.lower()
        if not text:
            # logging.warning(f"No text found on page {page_no}")
            return {"paragraphs": [], "sections": []}

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        sections = []
        paragraphs_list = []
        current_section = None

        for i, paragraph in enumerate(paragraphs):
            if len(paragraph.split()) < 8 and paragraph.istitle():
                current_section = paragraph.strip()
                sections.append({current_section: "", f"summary of {current_section}": ""})
            elif current_section:
                sections[-1][current_section] += paragraph + " "
            else:
                paragraphs_list.append(paragraph)

        result = {}

        if sections:
            logging.info("System detects sections")
            for section in sections:
                section_title = list(section.keys())[0]
                section_text = section[section_title].strip()

                try:
                    summary = summarize_text(section_text)
                except Exception():
                    # logging.error(f"Error summarizing section '{section_title}' on page {page_no}: {str(e)}")
                    summary = "An error occurred, and summarization was not possible"

                section[f"summary of {section_title}"] = summary

            result["sections"] = sections
        if not sections and paragraphs_list:
            summarized_paragraphs = []
            for paragraph in paragraphs_list:
                try:
                    summary = summarize_text(paragraph)
                except Exception:
                    # logging.error(f"Error summarizing paragraph on page {page_no}: {str(e)}")
                    summary = "An error occurred, and summarization was not possible"

                summarized_paragraphs.append(
                    {"paragraph": paragraph, "summary": summary})

            result["paragraphs"] = summarized_paragraphs

        # duration = timedelta(seconds=time.perf_counter() - start_time)
        # logging.info(f"Summarization took: {duration}")

        return result

    except Exception as e:
        # logging.error(f"Error extracting text or reading page {page_no}: {str(page_error)}")
        return {"text": f"error reading page: {e}", "summary": "No summary available"}
