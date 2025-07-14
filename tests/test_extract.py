import io
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_extract_sample_pdf():
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 700, "Invoice Number: INV-12345")
    c.drawString(100, 680, "Invoice Date: 2024-07-10")
    c.drawString(100, 660, "Vendor: Acme Corp")
    c.drawString(100, 640, "Total Amount: 1025.75")
    c.save()
    buffer.seek(0)

    files = {"files": ("test_invoice.pdf", buffer, "application/pdf")}
    response = client.post("/extract", files=files)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    invoice = data[0]
    assert invoice["invoice_number"] == "INV-12345"
    assert invoice["invoice_date"] == "2024-07-10"
    assert invoice["vendor_name"] == "Acme Corp"
    assert abs(invoice["total_amount"] - 1025.75) < 0.01