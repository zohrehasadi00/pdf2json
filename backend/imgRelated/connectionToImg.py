from PIL import Image
from typing import List
from backend.imgRelated.text_from_img import extract_text_from_image


def visualLink(image: Image.Image, page_data: List[dict], page_number: int) -> str:
    extracted_text = extract_text_from_image(image)

    page_entry = next((entry for entry in page_data if entry.get("page") == page_number), None)

    if not page_entry or "data" not in page_entry or "paragraphs" not in page_entry["data"]:
        return "No related paragraph found"

    relevant_paragraphs = page_entry["data"]["paragraphs"]

    for paragraph in relevant_paragraphs:
        paragraph_text = paragraph["paragraph"]
        if extracted_text.lower() in paragraph_text.lower():
            return paragraph_text

    return "No related paragraph found"
