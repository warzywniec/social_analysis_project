from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

from app.db.session import SessionLocal
from app.models.headline import Headline
from app.models.site import Site
from app.schemas.headline import HeadlineSchema
from app.schemas.site import SiteSchema
from app.auth.dependencies import get_current_user

from app.export_import.exporter import export_headlines_to_json, export_headlines_to_xml
from app.export_import.importer import import_headlines_from_json, import_headlines_from_xml

from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.schemas.user import UserCreate, Token
from app.auth.utils import get_password_hash, verify_password, create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# HEADLINES

@router.get("/headlines/", response_model=List[HeadlineSchema])
def get_headlines(
    date: Optional[str] = Query(None, description="Exact year, e.g., '2022'"),
    emotion: Optional[str] = Query(None, description="Emotion, e.g., 'anger'"),
    headline_contains: Optional[str] = Query(None, description="Search in headline"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(Headline)

    if date:
        query = query.filter(Headline.date == date)
    if emotion:
        query = query.filter(Headline.emotion == emotion)
    if headline_contains:
        query = query.filter(Headline.headline.ilike(f"%{headline_contains}%"))

    return query.offset(skip).limit(limit).all()


# SITES

@router.get("/sites/", response_model=List[SiteSchema])
def get_sites(
    date: Optional[str] = Query(None, description="Year, e.g., '2022'"),
    category: Optional[str] = Query(None, description="Exact category name"),
    category_contains: Optional[str] = Query(None, description="Partial category match"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Site)

    if date:
        query = query.filter(Site.date == date)
    if category:
        query = query.filter(Site.category == category)
    if category_contains:
        query = query.filter(Site.category.ilike(f"%{category_contains}%"))

    return query.offset(skip).limit(limit).all()


@router.get("/emotion-summary/")
def get_emotion_summary(
    year: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    emotion: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = (
        db.query(
            Site.category,
            Site.date,
            Headline.emotion,
            func.count(Headline.id).label("count")
        )
        .join(Headline, Headline.site_id == Site.id)
    )

    if year:
        query = query.filter(Site.date == year)
    if category:
        query = query.filter(Site.category == category)
    if emotion:
        query = query.filter(Headline.emotion == emotion)

    result = (
        query.group_by(Site.category, Site.date, Headline.emotion)
             .order_by(Site.category, Site.date, Headline.emotion)
             .all()
    )

    return [
        {
            "category": row[0],
            "year": row[1],
            "emotion": row[2],
            "count": row[3]
        }
        for row in result
    ]

@router.post("/export/json")
def export_json(current_user=Depends(get_current_user)):
    export_headlines_to_json()
    return {"message": "Exported to JSON"}

@router.post("/export/xml")
def export_xml(current_user=Depends(get_current_user)):
    export_headlines_to_xml()
    return {"message": "Exported to XML"}

@router.post("/import/json")
def import_json(current_user=Depends(get_current_user)):
    import_headlines_from_json()
    return {"message": "Imported from JSON"}

@router.post("/import/xml")
def import_xml(current_user=Depends(get_current_user)):
    import_headlines_from_xml()
    return {"message": "Imported from XML"}

# Przekierowanie z / na /login
@router.get("/", include_in_schema=False)
def redirect_root():
    return RedirectResponse(url="/login")

# Rejestracja użytkownika
@router.post("/register", response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        return {"access_token": "", "token_type": "bearer"}  # Można też rzucić HTTPException

    hashed_pw = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.username})
    return {"access_token": token, "token_type": "bearer"}

# Logowanie użytkownika
@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        return {"access_token": "", "token_type": "bearer"}  # lub raise HTTPException(...)
    
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
