from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pipeline.api import pdf_processing

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

app.include_router(pdf_processing.router, prefix="/api/pdf-processing", tags=["PDF Processing"])


@app.get("/", tags=["Health Check"])
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "OK", "message": "The API is up and running!"}
