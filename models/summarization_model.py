from transformers import pipeline


class SummarizationModel:
    """Summarization model using Hugging Face pipeline."""

    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        """
        Summarize the input text.

        Args:
            text (str): Input text to summarize.
            max_length (int): Maximum length of summary.
            min_length (int): Minimum length of summary.

        Returns:
            str: Summarized text.
        """
        summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]["summary_text"]
