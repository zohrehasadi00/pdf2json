import openai
import logging

api_key = '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'
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
client = openai.OpenAI(api_key=api_key)


def summarize_text(text):
    logger.info("Summarization started")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes texts."},
            {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
        ],
        max_tokens=150,
        temperature=0.5,
    )

    summary = response.choices[0].message.content.strip()
    return summary
