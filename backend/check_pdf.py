from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.layout import LTTextBox, LTChar
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFTextExtractionNotAllowed

import logging


# Filter out specific warning about missing CropBox
class CropBoxWarningFilter(logging.Filter):
    def filter(self, record):
        return "CropBox missing from /Page" not in record.getMessage()


# Attach filter to the pdfminer logger
pdfminer_logger = logging.getLogger("pdfminer")
pdfminer_logger.addFilter(CropBoxWarningFilter())

# Optional: Set log level lower to avoid other warnings
pdfminer_logger.setLevel(logging.ERROR)


def check(pdf_path):
    try:
        extracted_text = extract_text(pdf_path)
        if extracted_text.lower().startswith("(cid:"):
            return True

        with open(pdf_path, "rb") as f:
            parser = PDFParser(f)
            doc = PDFDocument(parser)
            parser.set_document(doc)
            if not doc.is_extractable:
                return True
            rsrcmgr = PDFResourceManager()
            device = PDFPageAggregator(rsrcmgr, laparams=None)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
                layout = device.get_result()
                for element in layout:
                    if isinstance(element, LTTextBox):
                        for text_line in element:
                            for char in text_line:
                                if isinstance(char, LTChar) and "cid" in char.fontname:
                                    return True
    except (PDFSyntaxError, PDFTextExtractionNotAllowed):
        return True
    return False
