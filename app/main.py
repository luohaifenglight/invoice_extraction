from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(title="Invoice Extraction API")

app.include_router(endpoints.router)
