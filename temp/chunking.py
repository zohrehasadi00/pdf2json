import PyPDF2
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tokenize import sent_tokenize

# Download NLTK resources (run this only once)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text ()
        return text


def chunk_text(text):
    sentences = sent_tokenize(text)
    tokenized_sentences = [word_tokenize(sent) for sent in sentences]
    tagged_sentences = [pos_tag(sent) for sent in tokenized_sentences]

    chunked_sentences = []
    for tagged_sentence in tagged_sentences:
        chunked_sentence = ne_chunk(tagged_sentence)
        chunked_sentences.append(chunked_sentence)

    return chunked_sentences


# Replace with your PDF file path
pdf_file_path = 'Big Data and BI - ICA - 2022 (1).pdf'

# Extract text from the PDF file
extracted_text = extract_text_from_pdf(pdf_file_path)

# Perform chunking on the extracted text
chunked_text = chunk_text(extracted_text)

# Display the chunked text
for sentence in chunked_text:
    print(sentence)