from pathlib import Path
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from backend.structure_json import process_pdf_text_only
from backend.structure_json import process_pdf_image_only
import os

router = APIRouter()


@router.post("/pdf-processing/text", tags=["Text Processing"])
async def extract_text_from_pdf(file: UploadFile):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    temp_file = Path(os.path.join(os.getenv("TEMP", "/tmp"), file.filename))
    with open(temp_file, "wb") as f:
        f.write(await file.read())

    result = {"Status": "Success", "Pages": []}

    try:
        text_result = process_pdf_text_only(temp_file)
        image_result = process_pdf_image_only(temp_file)

        for text_page, image_page in zip(text_result["Pages"], image_result["Pages"]):
            result["Pages"].append({
                "Page": text_page["Page"],
                "Text": text_page["Text"],
                "Summary": text_page["Summary"],
                "Images": image_page["Images"]
            })

        os.remove(temp_file)
        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

    finally:
        temp_file.unlink()
