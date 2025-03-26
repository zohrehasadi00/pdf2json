from fastapi.responses import JSONResponse
from gui import papaias
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import io
import threading
from api.api import extract_text_from_pdf
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
# import time
app = FastAPI(
    title="Document Processing API",
    description="An API for processing PDFs",
    version="1.0.0"
)
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/pdf-processing/text")
async def process_pdf(file: UploadFile = File(...)):
    """
    Endpoint to process a PDF file and extract text.
    """
    try:
        content = await file.read()
        result = {
            file.filename: f"is saved in {save_to}"
        }
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

async def main():
    server_thread = threading.Thread(target=uvicorn.run, kwargs={"app": app, "host": "127.0.0.1", "port": 8000}) # "127.0.0.1"
    server_thread.daemon = True
    server_thread.start()
    print("API server started. Now launching GUI...")
    gui = papaias()
    pdf_path = gui[0]
    global save_to
    save_to = gui[1]
    if pdf_path:
        file_name = pdf_path.name
        file_content = pdf_path.read_bytes()
        upload_file = UploadFile(filename=file_name, file=io.BytesIO(file_content))
        # print(f"Selected PDF: {pdf_path}")
        print("Sending file to the API...")
        await extract_text_from_pdf(upload_file, save_to)
    else:
        print("No file selected. Exiting.")
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
