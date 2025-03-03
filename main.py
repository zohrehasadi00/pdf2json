from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import api

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


# @app.post("/api/pdf-processing/save-response")
# async def save_response(response: dict):
#     """
#     Endpoint to save JSON response to a file.
#     """
#     output_path = Path(r"C:\Users\zohre\bachelorT\MediLink\example\response.json")
#     with open(output_path, "w", encoding="utf-8") as json_file:
#         json.dump(response, json_file, ensure_ascii=False, indent=4)
#
#     return {"status": "Success", "message": "Response saved successfully."}

