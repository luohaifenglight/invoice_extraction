from typing import Optional, List
from app.models.invoice import InvoiceData
from app.utils.pdf_utils import (
    extract_text_from_pdf,
    is_scanned_pdf,
    ocr_pdf,
)
import re
from dateutil import parser


def extract_invoice_data(file_bytes: bytes) -> InvoiceData:
    warnings: List[str] = []

    text = extract_text_from_pdf(file_bytes)
    if is_scanned_pdf(text):
        text = ocr_pdf(file_bytes)

    invoice_number = _extract_invoice_number(text)
    if not invoice_number:
        warnings.append("Invoice number not found")

    invoice_date = _extract_invoice_date(text)
    if not invoice_date:
        warnings.append("Invoice date not found")

    vendor_name = _extract_vendor_name(text)
    if not vendor_name:
        warnings.append("Vendor name not found")

    total_amount = _extract_total_amount(text)
    if total_amount is None:
        warnings.append("Total amount not found")

    return InvoiceData(
        invoice_number=invoice_number,
        invoice_date=invoice_date,
        vendor_name=vendor_name,
        total_amount=total_amount,
        warnings=warnings if warnings else None,
    )


def _extract_invoice_number(text: str) -> Optional[str]:
    patterns = [
        r"Invoice\s*Number[:\s]*([A-Za-z0-9\-]+)",
        r"Invoice\s*No\.?[:\s]*([A-Za-z0-9\-]+)",
        r"Invoice\s*#[:\s]*([A-Za-z0-9\-]+)",
        r"Inv\s*No\.?[:\s]*([A-Za-z0-9\-]+)",
        r"Invoice\s*ID[:\s]*([A-Za-z0-9\-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _extract_invoice_date(text: str) -> Optional[str]:
    date_patterns = [
        r"Invoice\s*Date[:\s]*([0-9]{4}[-/][0-9]{2}[-/][0-9]{2})",
        r"Date[:\s]*([0-9]{4}[-/][0-9]{2}[-/][0-9]{2})",
        r"Invoice\s*Date[:\s]*([0-9]{2}[-/][0-9]{2}[-/][0-9]{4})",
        r"Date[:\s]*([0-9]{2}[-/][0-9]{2}[-/][0-9]{4})",
        r"Date[:\s]*([A-Za-z]{3,9}\s+\d{1,2},\s+\d{4})",
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            date_str = match.group(1).strip()
            normalized = _normalize_date(date_str)
            if normalized:
                return normalized
            else:
                return date_str
    return None


def _normalize_date(date_str: str) -> Optional[str]:
    try:
        dt = parser.parse(date_str)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None


def _extract_vendor_name(text: str) -> Optional[str]:
    patterns = [
        r"Vendor[:\s]*([A-Za-z0-9 &.,\-]+)",
        r"From[:\s]*([A-Za-z0-9 &.,\-]+)",
        r"Supplier[:\s]*([A-Za-z0-9 &.,\-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines:
        for line in lines[:5]:
            if not re.search(r"(invoice|date|total|amount|number|no\.?|#)", line, re.I):
                return line
    return None


def _extract_total_amount(text: str) -> Optional[float]:
    patterns = [
        r"Total\s*Amount[:\s]*\$?([0-9,]+\.\d{2})",
        r"Amount\s*Due[:\s]*\$?([0-9,]+\.\d{2})",
        r"Balance\s*Due[:\s]*\$?([0-9,]+\.\d{2})",
        r"Total[:\s]*\$?([0-9,]+\.\d{2})",
        r"Amount[:\s]*\$?([0-9,]+\.\d{2})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount_str = match.group(1).replace(",", "")
            try:
                return float(amount_str)
            except ValueError:
                continue

    money_matches = re.findall(r"\$?([0-9,]+\.\d{2})", text)
    amounts = []
    for m in money_matches:
        try:
            amounts.append(float(m.replace(",", "")))
        except ValueError:
            continue
    if amounts:
        return max(amounts)
    return None