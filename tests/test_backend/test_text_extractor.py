import pytest
from pathlib import Path
from backend.text_extractor import extract_text_and_summarize


# Use a real PDF file for testing
@pytest.fixture
def sample_pdf():
    pdf_path = Path("C:/Users/zohre/OneDrive/Desktop/bachelorArbeit/pdf_example/The_Basics_of_Anesthesia_7th_Edition.pdf")
    # Check if the PDF exists
    if not pdf_path.exists():
        pytest.fail(f"PDF file {pdf_path} does not exist.")
    return pdf_path


def test_extract_text_and_summarize(sample_pdf):
    # Assuming extract_text_and_summarize correctly extracts and summarizes text from the PDF
    result = extract_text_and_summarize(sample_pdf)
    print(result)

    # Ensure result is a list
    assert isinstance(result, list)

    # Ensure the list contains information for each page
    assert len(result) > 0  # Ensure there are pages extracted

    # Check for each page
    for page in result:
        # Each page should contain the expected keys: 'PageNumber', 'Text', 'Summary'
        assert "PageNumber" in page
        assert "Text" in page
        assert "Summary" in page

        # Ensure the Text is not empty for any page
        assert page["Text"].strip() != ""

        # Optionally, check the Summary is not empty
        assert page["Summary"].strip() != ""

        # Ensure the PageNumber corresponds to the correct page number
        assert isinstance(page["PageNumber"], int)
        assert page["PageNumber"] > 0
