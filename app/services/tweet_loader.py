from datasets import load_dataset
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dateutil import parser  # do parsowania timestampów
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

# Wczytaj dane z Exorde
dataset = load_dataset("Exorde/exorde-social-media-december-2024-week1", split="train")

# Filtruj tylko dane z pierwszego tygodnia grudnia
filtered_dataset = dataset.filter(lambda x: x["timestamp"].startswith("2024-12-0"))

# Ogranicz do 100 wpisów (dla szybkości testów)
sample_data = filtered_dataset.select(range(100))

# Wstawianie do bazy
for item in sample_data:
    try:
        created_at = parser.parse(item["timestamp"])
    except Exception:
        created_at = datetime.now()  # fallback

    tweet = Tweet(
        text=item.get("text", ""),
        label="unlabeled",  # jeśli masz inne pole do oznaczenia, zmień tutaj
        created_at=created_at
    )
    session.add(tweet)

session.commit()
print("Wczytano tweety z Exorde do bazy.")
