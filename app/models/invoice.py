from typing import List, Optional
from pydantic import BaseModel


class InvoiceData(BaseModel):
    invoice_number: Optional[str]
    invoice_date: Optional[str]
    vendor_name: Optional[str]
    total_amount: Optional[float]
    warnings: Optional[List[str]] = None