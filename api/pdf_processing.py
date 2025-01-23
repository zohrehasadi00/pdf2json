from pathlib import Path
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from backend.structure_json import process_pdf
import os
import tempfile
import shutil

router = APIRouter()


@router.post("/text", tags=["Text Processing"])
async def extract_text_from_pdf(file: UploadFile):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # virtual copy
    temp_dir = tempfile.mkdtemp()

    temp_file_path = Path(temp_dir) / file.filename

    try:
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())
        print(temp_file_path)
        result = {"Status": "Success", "Pages": []}
        text_result = process_pdf(temp_file_path)
        image_result = {"Pages": []}

        for text_page, image_page in zip(text_result["Pages"], image_result["Pages"]):
            result["Pages"].append({
                "Page": text_page["Page"],
                "Text": text_page["Text"],
                "Summary": text_page["Summary"],
                "Images": image_page["Images"]
            })

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
