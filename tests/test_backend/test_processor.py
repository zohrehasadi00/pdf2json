from old.structure_json import process_pdf_text_only

def test_process_pdf_text_only(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_text("Test PDF content")

    result = process_pdf_text_only(pdf_path)
    assert isinstance(result, dict)
    assert "Title" in result
    assert "Pages" in result
    assert isinstance(result["Pages"], list)
    assert len(result["Pages"]) > 0
