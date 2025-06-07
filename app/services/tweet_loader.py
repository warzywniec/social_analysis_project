import json
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.db.session import engine, SessionLocal, Base
from app.models.tweet import Tweet

# Model Tweet (upewnij się, że nie masz duplikatu w app.models.tweet)
class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    label = Column(String)
    created_at = Column(DateTime)

# DB setup
session = SessionLocal()

# Load data from local JSON file
with open('app/data/sites_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Insert data into database
for item in dataset:
    try:
        created_at = datetime.fromisoformat(item.get("created_at", datetime.now().isoformat()))
    except Exception:
        created_at = datetime.now()  # fallback

    tweet = Tweet(
        text=item.get("text", ""),
        source=item.get("source", "unknown"),
        lang=item.get("lang", "und"),
        label=item.get("label", "unlabeled"),
        created_at=created_at
    )
    session.add(tweet)

session.commit()
print("Wczytano dane z lokalnego pliku JSON do bazy.")
