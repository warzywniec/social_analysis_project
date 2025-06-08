from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import SessionLocal
from app.models.headline import Headline
from app.models.site import Site
from app.schemas.headline import HeadlineSchema
from app.schemas.site import SiteSchema
from app.auth.dependencies import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# HEADLINES

@router.get("/headlines/", response_model=List[HeadlineSchema])
def get_headlines(date: Optional[str] = None, emotion: Optional[str] = None, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    query = db.query(Headline)
    if date:
        query = query.filter(Headline.date == date)
    if emotion:
        query = query.filter(Headline.emotion == emotion)
    return query.all()

# SITES

@router.get("/sites/", response_model=List[SiteSchema])
def get_sites(date: Optional[str] = None, category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Site)
    if date:
        query = query.filter(Site.date == date)
    if category:
        query = query.filter(Site.category == category)
    return query.all()
