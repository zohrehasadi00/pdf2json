import os
import tempfile
import shutil
import json
import logging
from pathlib import Path
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from backend.pdf_processor import process_pdf

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/text", tags=["Text Processing"])
async def extract_text_from_pdf(file: UploadFile):
    logger.info(f"Received file: {file.filename}")

    if not file.filename.endswith(".pdf"):
        logger.warning(f"Invalid file format: {file.filename}")
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    temp_dir = tempfile.mkdtemp()
    temp_file_path = Path(temp_dir) / file.filename
    logger.debug(f"Temporary file path: {temp_file_path}")

    try:

        with open(temp_file_path, "wb") as temp_file:
            file_data = await file.read()
            temp_file.write(file_data)
            logger.info(f"Saved file to temporary path: {temp_file_path} (Size: {len(file_data)} bytes)")

        logger.info("Processing PDF...")
        pdf_results = process_pdf(temp_file_path)
        logger.debug(f"Extracted information: {pdf_results}")

        output_path = Path(r"C:\Users\zohre\bachelorT\MediLink\reports\response.json")
        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump(pdf_results, json_file, ensure_ascii=False, indent=4)
        logger.info(f"Saved JSON response to: {output_path}")

        logger.info("PDF processing completed successfully.")
        return JSONResponse(content=pdf_results)


    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logger.debug(f"Deleted temporary file: {temp_file_path}")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            logger.debug(f"Deleted temporary directory: {temp_dir}")
