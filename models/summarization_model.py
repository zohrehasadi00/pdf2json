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

""" 
#TEST: 

summ = SummarizationModel()
t = "The golden rays of the setting sun bathed the landscape in a warm, amber glow. Birds chirped melodiously, returning to their nests after a long day. A gentle breeze rustled through the trees, carrying with it the earthy scent of nature. In the distance, the silhouette of mountains stood proudly against the colorful sky, painted with shades of orange, pink, and purple. A lone deer grazed peacefully in the meadow, undisturbed by the serenity surrounding it. The quiet hum of life filled the air, a soothing symphony of nature’s harmony. This tranquil moment, where time seemed to pause, reminded one of life’s simple yet profound beauty. It was a scene etched into memory, a picture of perfect calm and peace."
print(summ.summarize(text = t, max_length = 130, min_length = 30))
"""