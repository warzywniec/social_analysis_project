import pandas as pd
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.db.session import SessionLocal, Base
from app.models.gdelt import GDELTEntry

# Model GDELTEntry (upewnij się, że masz go w app.models.gdelt)
class GDELTEntry(Base):
    __tablename__ = "gdelt_entries"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    themes = Column(Text)
    locations = Column(Text)
    organizations = Column(Text)

# Setup DB session
session = SessionLocal()

# Load data from local CSV file
df = pd.read_csv('app/data/classified_headlines.csv')

# Insert data into database
for _, row in df.iterrows():
    try:
        entry_date = pd.to_datetime(row.get("date", datetime.now())).date()
    except Exception:
        entry_date = datetime.now().date()

    entry = GDELTEntry(
        date=entry_date,
        title=row.get("title", ""),
        source=row.get("source", ""),
        themes=row.get("themes", ""),
        locations=row.get("locations", ""),
        organizations=row.get("organizations", "")
    )
    session.add(entry)

session.commit()
print("Wczytano dane z lokalnego pliku CSV do bazy.")
