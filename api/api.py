import os
import json
import shutil
import socket
import logging
import requests
import tempfile
from pathlib import Path
from backend.pdf_processor import process_pdf
from fastapi import APIRouter, UploadFile, HTTPException

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter()

async def extract_text_from_pdf(file: UploadFile, save_to:Path):
    """
    Processes a PDF file, extracts text, and sends the file to the API.
    """
    logger.info(f"Received file: {file.filename}")
    url = "http://127.0.0.1:8000/api/pdf-processing/text"

    if not file.filename.endswith(".pdf"):
        logger.warning(f"Invalid file format: {file.filename}")
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    temp_dir = tempfile.mkdtemp()
    temp_file_path = Path(temp_dir) / file.filename

    try:
        with open(temp_file_path, "wb") as temp_file:
            file_data = await file.read()
            temp_file.write(file_data)

        pdf_results = process_pdf(temp_file_path)

        file_name = file.filename
        name_only = os.path.splitext(file_name)[0] + ".json"
        output_path = Path(save_to) / name_only

        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump(pdf_results, json_file, ensure_ascii=False, indent=4)

        with open(temp_file_path, "rb") as file_to_send:
            files = {"file": (file.filename, file_to_send, "application/pdf")}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            logger.info(f"API Response: {response.json()}")
        elif response.status_code == 404:
            logger.error(f"API Error 404: Not Found - URL might be incorrect.")
            actual_port = get_actual_api_port()
            logger.error(f"Make sure your FastAPI server is running on the correct port: {actual_port}")
        else:
            logger.error(f"API Error: {response.status_code} - {response.text}")

        # print(json.dumps(pdf_results, indent=4))
        return pdf_results

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


def get_actual_api_port():
    """
    Function to dynamically check the actual port on which the FastAPI server is running.
    """
    try:
        socket.setdefaulttimeout(1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("0.0.0.0", 0))  # 0 means OS picks an available port
        actual_port = s.getsockname()[1]
        s.close()
        return actual_port
    except socket.error as err:
        logger.error(f"Error detecting the port: {err}")
        return 8000  # fallback to default port if error occurs
