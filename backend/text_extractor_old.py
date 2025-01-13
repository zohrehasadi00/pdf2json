import PyPDF2
from pathlib import Path
from typing import List, Dict
from models.summarization_model import SummarizationModel

summarizer = SummarizationModel()


def extract_text_and_summarize(file_path: Path) -> List[Dict]:
    """
    Extract text and summarize it for each page of the PDF.
    """
    result = []
    try:
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            if not reader.pages:
                raise ValueError(f"The PDF file '{file_path}' has no pages.")

            for page_no, page in enumerate(reader.pages, start=1):
                try:
                    text = page.extract_text()
                    if text:
                        summary = summarizer.summarize(text, max_length=150, min_length=50)
                    else:
                        text = "No text available"
                        summary = "No summary available"
                    result.append({
                        "PageNumber": page_no,
                        "Text": text,
                        "Summary": summary,
                    })
                except Exception as page_error:
                    text = f"Error reading page: {page_error}"
                    summary = "No summary available"
    except Exception as e:
        raise Exception(f"Error extracting text: {str(e)}")

    return result


if __name__ == "__main__":
    pdf_path = Path(r"C:/Users/zohre/OneDrive/Desktop/bachelorArbeit/pdf_example/The_Basics_of_Anesthesia_7th_Edition.pdf")
    try:
        output = extract_text_and_summarize(pdf_path)
    except Exception as e:
        print(f"Error: {e}")

# if text:
#     cleaned_text = " ".join(text.replace("\n", " ").split())
#     if cleaned_text:  # Check if cleaned text is non-empty
#         try:
#             summary = summarizer.summarize(cleaned_text, max_length=150, min_length=50)
#         except IndexError as e:
#             summary = f"Error during summarization: {str(e)}"
#     else:
#         summary = "No text available to summarize."
# else:
#     summary = "No text found on this page."
#