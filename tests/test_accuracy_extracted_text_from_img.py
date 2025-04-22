import fitz
import io
import pytest
from pathlib import Path
from PIL import Image
from typing import List
from models.tesseract_ocr_model import TesseractOcrModel
from models.base_ocr_model import BaseOcrModel

def extract_images_from_pdf(pdf_path: Path) -> List[Image.Image]:
    """Extract images from a given PDF file."""
    images = []
    doc = fitz.open(str(pdf_path))
    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_data = base_image["image"]
            pil_image = Image.open(io.BytesIO(image_data)).convert("RGB")
            images.append(pil_image)
    return images

def compare_text_accuracy(real_text: str, extracted_text: str) -> float:
    """Compare real and extracted text to calculate accuracy."""
    real_words = real_text.split()
    extracted_words = extracted_text.split()
    common_words = set(real_words) & set(extracted_words)
    return (len(common_words) / max(len(real_words), 1)) * 100  # Percentage accuracy

def test_ocr_accuracy(pdf_path: Path, real_text: str):
    """Test OCR accuracy by extracting images, running OCR, and comparing text."""
    ocr_model = TesseractOcrModel(BaseOcrModel)
    images = extract_images_from_pdf(pdf_path)
    extracted_text = " ".join([ocr_model.predict(img) for img in images])
    accuracy = compare_text_accuracy(real_text, extracted_text)
    print(f"OCR Accuracy: {accuracy:.2f}%")
    return accuracy

@pytest.mark.parametrize("pdf_path, real_text", [
    (Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\test.pdf"),
     "Anesthesia ExplainedGeneral AnesthesiaUnder general anesthesia, you will be in a state of controlled "
     "unconsciousness during which you will not feel or remember anything that happens. This type of "
     "anesthesia is essential for a wide range of surgeries to ensure you experience no pain or awareness "
     "during the procedure. It is commonly used for operations on the heart, abdomen, and other major "
     "surgeries. General anesthesia is administered either through intravenous drugs or anesthetic gases "
     "that the patient breathes in. While under anesthesia, you cannot be woken until the drugs are stopped "
     "and their effects wear off. During this unconscious state, the medical team in the operating theater "
     "takes great care to monitor and protect your health, ensuring that the anesthetist stays close by at all times.")
])
def test_ocr_accuracy_param(pdf_path, real_text):
    accuracy = test_ocr_accuracy(pdf_path, real_text)
    assert accuracy > 30, f"OCR accuracy too low: {accuracy:.2f}%"