import nltk
from nltk.tokenize import sent_tokenize
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO

nltk.download('punkt_tab')

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()  # rsrcmgr = resource manager (such as fonts and images while processing a PDF)
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    try:
        with open(path, 'rb') as fp:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(fp, check_extractable=True):
                interpreter.process_page(page)

        text = retstr.getvalue()
        print("Extracted Text Preview: ", text[:500])
        sentences = sent_tokenize(text)
        print("Sentences Tokenized:", sentences[:5])

        output_text = ""
        for s in sentences:
            s = s.replace("-\n", "")
            lines = s.split("\n")
            for line in lines:
                if line.isupper():  # detect section titles
                    line = "--SECTION-- " + line
                    output_text += "\n\n" + line + "\n"
                else:
                    output_text += line
            output_text += "\n"

        device.close()
        retstr.close()

        return output_text

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""


converted_text = convert_pdf_to_txt(r"C:\Users\zohre\OneDrive\Desktop\bachelorArbeit\statics\sample_pdfs\krebs.pdf")
print(converted_text)
