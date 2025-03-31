from openai import OpenAI
from typing import List, Dict

client = OpenAI(
    api_key='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'
)


def detect_sections(text: str) -> List[Dict]:
    """Use GPT-4 to detect sections in a text document."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "You are a document analysis assistant. Identify and extract sections from the following text. Return each section with its title and content in JSON format."},
            {"role": "user", "content": f"Analyze this document text and identify all sections:\n\n{text}"}
        ],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content
