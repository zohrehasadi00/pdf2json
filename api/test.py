import os
import json
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from typing import Optional
from backend.pdf_processor import process_pdf

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/process-pdf/")
async def extract_text_from_pdf(pdf_path: str, save_to: str):
    try:
        # Validate paths
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            raise HTTPException(
                status_code=404,
                detail="PDF file not found"
            )

        # Check if file is PDF
        if not pdf_path.lower().endswith('.pdf'):
            logger.error(f"Invalid file format: {pdf_path}")
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )

        # Ensure save_to directory exists
        save_path = Path(save_to)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Process the PDF
        result = process_pdf(Path(pdf_path))

        # Save results as JSON
        output_file = save_path.with_suffix('.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        logger.info(f"Results saved to: {output_file}")

        return {
            "status": "success",
            "message": "PDF processed successfully",
            "result_path": str(output_file),
            "status_code": 200
        }

    except HTTPException:
        raise  # Re-raise already handled exceptions

    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF: {str(e)}"
        )