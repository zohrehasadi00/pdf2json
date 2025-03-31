from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


def segment_paragraphs_textrank(text, language):
    """
    Segments text into coherent paragraphs using TextRank.

    Args:
        text (str): The input text.
        language (str): Language of the text ("english" or "german").

    Returns:
        List[str]: List of extracted paragraphs.
    """
    if language == "en":
        language = "english"
    elif language == "de":
        language = "german"

    if language not in ["english", "german"]:
        raise ValueError("Only 'english' and 'german' languages are supported.")

    parser = PlaintextParser.from_string(text, Tokenizer(language))
    summarizer = LexRankSummarizer()

    num_sentences = max(1, len(parser.document.sentences) // 4)  # Dynamically adjust paragraph size

    key_sentences = summarizer(parser.document, num_sentences)

    paragraphs = []
    current_paragraph = []

    for sentence in parser.document.sentences:
        current_paragraph.append(str(sentence))

        if sentence in key_sentences:
            paragraphs.append(" ".join(current_paragraph))
            current_paragraph = []

    if current_paragraph:
        paragraphs.append(" ".join(current_paragraph))

    return paragraphs
