import logging
from openai import OpenAI
from secret import OPENAI_KEY
from langdetect import detect


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
client = OpenAI(api_key=OPENAI_KEY)


def summarize_text(text):
    language = detect(text)
    language_prompts = {
        "en": "Please summarize the following text in English:\n\n{text}",
        "de": "Bitte fassen Sie den folgenden Text auf Deutsch zusammen:\n\n{text}",
    }
    if language in language_prompts:
        prompt = language_prompts[language]
    else:
        prompt = f"Please summarize the following text (detected language: {language}):\n\n{{text}}"

    prompt = prompt.format(text=text)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes texts."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.5,
    )

    summary = response.choices[0].message.content.strip()
    return summary
