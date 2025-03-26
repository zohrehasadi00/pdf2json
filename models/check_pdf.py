import re
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBox, LTChar
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFPageInterpreter


def check(pdf_path):
    try:
        extracted_text = extract_text(pdf_path)
        if re.search(r"cid:\d+", extracted_text):
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
