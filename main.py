import io
import os
import time
import logging
import uvicorn
import threading
from gui import papaias
from datetime import timedelta
from api.api import extract_text_from_pdf
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
save_to = None
app = FastAPI(
    title="Document Processing API",
    description="An API for processing PDFs",
    version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


@app.post("/api/pdf-processing/text")
async def process_pdf(file: UploadFile = File(...)):
    try:
        result = {
            file.filename: f"is saved in {save_to}"
        }
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


async def main():
    global save_to
    try:
        logging.info("API server started ...")
        server_thread = threading.Thread(target=uvicorn.run,
                                         kwargs={"app": app, "host": "0.0.0.0", "port": 8000})
        server_thread.daemon = True
        server_thread.start()

    except Exception as e:
        logging.info(f"Connection to the uvicorn was not possible\n{e}")

    logging.info("Launching GUI ...")

    gui = papaias()
    start_time = time.perf_counter()

    if not gui:
        logging.info("User canceled the process.")

    else:

        pdf_path = gui[0]
        save_to = Path(__file__).resolve().parent / "results"

        if pdf_path:
            file_name = pdf_path.name
            file_content = pdf_path.read_bytes()
            upload_file = UploadFile(filename=file_name, file=io.BytesIO(file_content))
            await extract_text_from_pdf(upload_file, save_to)
        else:
            logging.info("No file has been selected ... Exiting")

    duration = timedelta(seconds=time.perf_counter() - start_time)
    logging.info(f"Processing the pdf took: {duration}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
