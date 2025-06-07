# app/api/analysis.py

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from collections import Counter
from app.db.session import get_db
from app.models.tweet import Tweet
from app.models.gdelt import GDELTEntry

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.get("/summary")
def get_summary(
    start_date: datetime = Query(..., description="Początkowa data zakresu"),
    end_date: datetime = Query(..., description="Końcowa data zakresu"),
    db: Session = Depends(get_db)
):
    # --- Tweets: najczęstsze emocje ---
    tweets = db.query(Tweet).filter(Tweet.created_at.between(start_date, end_date)).all()
    tweet_labels = Counter([t.label for t in tweets if t.label])

    # --- GDELT: najczęstsze tematy ---
    gdelt_entries = db.query(GDELTEntry).filter(GDELTEntry.date.between(start_date.date(), end_date.date())).all()
    all_themes = []
    for entry in gdelt_entries:
        if entry.themes:
            all_themes += [theme.strip() for theme in entry.themes.split(';') if theme.strip()]

    gdelt_theme_counts = Counter(all_themes)

    return {
        "tweets_summary": tweet_labels.most_common(10),
        "gdelt_summary": gdelt_theme_counts.most_common(10)
    }
