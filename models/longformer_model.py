import os
import warnings
from transformers import pipeline
import logging
import time
from datetime import timedelta

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# summarizer = pipeline("summarization", model="facebook/bart-large-cnn") # 0:00:20.707973
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")  # 0:00:13.097513


def summarization(text, max_length=200, min_length=50, tokenizer=None, chunk_size=1024):
    if len(text) < min_length:
        logger.info("Text is too short to summarize. Returning original text.")
        return text

    start_time = time.perf_counter()
    summary_parts = []

    try:
        if tokenizer is None:
            tokenizer = summarizer.tokenizer

        while len(tokenizer.encode(text)) > chunk_size:
            chunk = text[:chunk_size]
            text = text[chunk_size:]

            summary_chunk = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            summary_parts.append(summary_chunk[0]["summary_text"])

        if len(text) > 0:
            summary_chunk = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            summary_parts.append(summary_chunk[0]["summary_text"])

        full_summary = " ".join(summary_parts)

        duration = timedelta(seconds=time.perf_counter() - start_time)
        logger.info(f"Summarization completed in {duration}")
        return full_summary

    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        return text
