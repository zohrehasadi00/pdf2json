from transformers import pipeline
from typing import List


class SummarizationModel:
    """Summarization model using Hugging Face pipeline."""

    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    @staticmethod
    def split_text(text: str, max_tokens: int = 1024) -> List[str]:
        """
        Split the text into smaller chunks within the max token limit.

        Args:
            text (str): The text to split.
            max_tokens (int): The maximum token length for each chunk.

        Returns:
            List[str]: List of text chunks.
        """
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            current_length += len(word) + 1  # Adding 1 for the space
            if current_length > max_tokens:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word) + 1
            else:
                current_chunk.append(word)

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def summarize(self, text: str, max_length, min_length) -> str:
        """
        Summarize the input text.

        Args:
            text (str): Input text to summarize.
            max_length (int): Maximum length of summary.
            min_length (int): Minimum length of summary.

        Returns:
            str: Summarized text.
        """
        tokenizer = self.summarizer.tokenizer
        token_count = len(tokenizer.encode(text, return_tensors="pt")[0])
        # token_count = len(self.summarizer.tokenizer.encode(text))

        if token_count <= 1024:
            summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]["summary_text"]
        else:
            chunks = self.split_text(text, max_tokens=1024)
            summaries = [self.summarize(chunk, max_length=max_length, min_length=min_length) for chunk in chunks]
            return " ".join(summaries)

# text = "asset"
# summarizer = SummarizationModel()
# summary = summarizer.summarize(text)
# print("Final Summary:\n", summary)
# TODO: put max length = max length of input
