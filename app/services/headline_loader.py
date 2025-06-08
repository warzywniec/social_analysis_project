import csv
from app.models.headline import Headline
from app.db.session import SessionLocal

def load_headlines_from_csv(filepath: str = "app/data/classified_headlines.csv"):
    db = SessionLocal()
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            headline = Headline(
                headline=row["headline"],
                date=row["date"],
                emotion=row["emotion"]
            )
            db.add(headline)
        db.commit()
    db.close()
