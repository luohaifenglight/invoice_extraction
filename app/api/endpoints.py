from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List

from app.services.extractor import extract_invoice_data
from app.services.llm_service import analyze_invoice_with_llm
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


@router.post("/extract_with_llm")
async def extract_with_llm(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        content = await file.read()
        try:
            invoice_data = extract_invoice_data(content)
            # 传入提取字段和全文给LLM做智能分析
            from app.utils.pdf_utils import extract_text_from_pdf, is_scanned_pdf, ocr_pdf

            text = extract_text_from_pdf(content)
            if is_scanned_pdf(text):
                text = ocr_pdf(content)

            llm_analysis = analyze_invoice_with_llm(invoice_data.dict(), text)

            combined_result = invoice_data.dict()
            combined_result["llm_analysis"] = llm_analysis

            results.append(combined_result)
        except Exception as e:
            results.append({"error": f"Failed to process {file.filename}: {str(e)}"})
    return JSONResponse(content=results)
