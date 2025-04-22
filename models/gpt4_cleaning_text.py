from openai import OpenAI
from secret import OPENAI_KEY


def cleaning(text, model="gpt-4o"):
    client = OpenAI(api_key=OPENAI_KEY)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": (
                        "Clean this text by removing extra whitespace, fixing typos, and improving readability while preserving meaning. "
                        "Normalize hyphenated line-breaks in words (e.g., aufklä-rungsgesprächs ➝ aufklärungsgesprächs, ef-fective ➝ effective), "
                        "and reconstruct all broken compound words accordingly. "
                        "Return only cleaned text from ALL PAGES. If a word can't be cleaned, return it as-is."
                    )
                 },
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return text
