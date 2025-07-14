# Invoice Extraction API

## Overview

This service extracts structured invoice data from scanned and digital PDF invoices.

## Features

- Detects scanned (image-based) vs digital (text-based) PDFs.
- Extracts invoice number, date, vendor name, and total amount.
- REST API with `/extract` and `/health` endpoints.
- REST API `/extract_with_llm` endpoints to summarize with AI.
- Returns JSON output.
- Includes automated tests.

## Requirements

- Python 3.10+
- Tesseract OCR installed (for OCR on scanned PDFs)
- Poppler utils installed (for PDF to image conversion)

## Installation

1. Clone the repo:

```bash
git clone <repo-url>
cd <repo-dir>
```

2.Install system dependencies:
On Ubuntu/Debian:
```
sudo apt-get update
sudo apt-get install -y poppler-utils tesseract-ocr libtesseract-dev libleptonica-dev pkg-config
```
3.Create and activate virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```
4.Install Python dependencies:
```
pip install -r requirements.txt
```
5.Running the app
```
uvicorn app.main:app --reload
The API will be available at http://localhost:8000.
```

6.Docker
Build and run with Docker:

```
docker build -t invoice-extractor .
docker run -p 8000:8000 invoice-extractor
```
7.Limitations & Improvements
```
Extraction relies on regex heuristics; may fail on diverse invoice formats.
OCR accuracy depends on image quality.
Vendor name extraction is heuristic and may be inaccurate.
Could improve with ML models or LLMs for better parsing.
Stretch goal: extract line items, integrate LLM for semantic understanding.
```