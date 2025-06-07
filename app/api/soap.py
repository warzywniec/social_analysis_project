from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from typing import List

router = APIRouter(prefix="/soap/news", tags=["SOAP (Mock) - GDELT"])

class NewsEntryIn(BaseModel):
    date: date
    title: str = ""
    source: str = ""
    themes: str = ""
    locations: str = ""
    organizations: str = ""

@router.post("/entries")
def receive_news(entries: List[NewsEntryIn]):
    print(f"[SOAP] Odebrano {len(entries)} wpisów prasowych (GDELT).")
    for entry in entries[:3]:
        print(f"{entry.date} | {entry.source} | Tematy: {entry.themes[:60]}")
    return {"status": "ok", "received": len(entries)}
