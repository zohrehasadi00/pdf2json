from openai import OpenAI


def cleaning(text, model="gpt-4"):  # gpt-4-turbo
    client = OpenAI(
        api_key='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')
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": "Clean this text by removing extra whitespace, fixing typos, and improving readability while preserving meaning. Return only cleaned text."},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return text
