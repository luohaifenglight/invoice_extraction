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