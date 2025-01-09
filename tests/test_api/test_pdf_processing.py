import pytest
from fastapi.testclient import TestClient
from main import app
from pathlib import Path

client = TestClient(app)

@pytest.fixture
def sample_pdf(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
        f.write(b"2 0 obj\n<< /Type /Pages /Count 1 /Kids [3 0 R] >>\nendobj\n")
        f.write(b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]\n")
        f.write(b"/Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 44 >>\n")
        f.write(b"stream\nBT\n/F1 24 Tf\n100 700 Td\n(Text Page) Tj\nET\nendstream\n")
        f.write(b"endobj\nxref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n")
        f.write(b"0000000066 00000 n \n0000000114 00000 n \n0000000178 00000 n \n")
        f.write(b"trailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n308\n%%EOF")
    return pdf_path

def test_api_extract_text_from_pdf(sample_pdf):
    with open(sample_pdf, "rb") as f:
        response = client.post("/api/pdf-processing/text", files={"file": ("sample.pdf", f, "application/pdf")})
    assert response.status_code == 200
    data = response.json()
    assert "Title" in data
    assert "Pages" in data
    assert isinstance(data["Pages"], list)
