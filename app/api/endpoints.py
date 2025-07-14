from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List

from app.services.extractor import extract_invoice_data
from app.models.invoice import InvoiceData

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/extract")
async def extract(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        content = await file.read()
        try:
            invoice_data = extract_invoice_data(content)
            results.append(invoice_data.dict())
        except Exception as e:
            results.append({"error": f"Failed to process {file.filename}: {str(e)}"})
    return JSONResponse(content=results)