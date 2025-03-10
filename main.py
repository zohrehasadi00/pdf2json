import pytesseract

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import api
from gui import papaias
import subprocess, requests, time, logging

logging.getLogger("torch").setLevel(logging.WARNING)  # Suppress info logs from torch
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)

app = FastAPI(
    title="Document Processing API",
    description="An API for processing PDFs (text extraction and summarization).",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api/pdf-processing", tags=["PDF Processing"])


@app.get("/", tags=["Health Check"])
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "OK", "message": "The API is up and running!"}


# curl.exe -X POST "http://127.0.0.1:8000/api/pdf-processing/text" -F "file=@C:/Users/zohre/OneDrive/Desktop/bachelorArbeit/pdf_example/IntroductionToAnaesthesia.pdf"
"""
if __name__ == "__main__":
    
    server_process = subprocess.Popen(["uvicorn", "main:app", "--reload"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print("Starting FastAPI server...")
    while True:
        output_line = server_process.stdout.readline() 
        # stucks here: output_line = server_process.stdout.readline()
        if output_line == "" and server_process.poll() is not None:
            logging.error("FastAPI server startup failed or terminated unexpectedly.")
            break
        if "Application startup complete." in output_line:
            print("FastAPI is running!")
            break
        time.sleep(0.5)

    pdf_path = papaias()
    logging.info("got the pdf path")

    if pdf_path:
        url = "http://127.0.0.1:8000/api/pdf-processing/text"
        files = {"file": open(pdf_path, "rb")}

        response = requests.post(url, files=files)
        logging.info("response has been saved")
"""
