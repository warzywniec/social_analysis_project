from fastapi import FastAPI
from app.api import rest, soap, analysis

app = FastAPI(title="Social & News API Mock")

# Rejestracja endpointów
app.include_router(rest.router)
app.include_router(soap.router)
app.include_router(analysis.router)