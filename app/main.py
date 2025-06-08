# from fastapi import FastAPI
# from app.api import rest, soap, analysis

# app = FastAPI(title="Social & News API Mock")

# # Rejestracja endpointów
# app.include_router(rest.router)
# app.include_router(soap.router)
# app.include_router(analysis.router)

from fastapi import FastAPI
from app.db.init_db import init_db
from app.services.headline_loader import load_headlines_from_csv
from app.services.site_loader import load_sites_from_json
from app.api import rest, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()
    load_headlines_from_csv()
    load_sites_from_json()

@app.get("/")
def root():
    return {"message": "API działa!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lub ["http://localhost:3000"] żeby ograniczyć
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    

app.include_router(rest.router)

app.include_router(auth.router, prefix="/auth")

