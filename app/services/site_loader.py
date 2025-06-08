import json
from app.models.site import Site
from app.db.session import SessionLocal

def load_sites_from_json(filepath: str = "app/data/sites_dataset.json"):
    db = SessionLocal()
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for entry in data:
            site = Site(
                category=entry["category"],
                date=entry["date"]
            )
            db.add(site)
        db.commit()
    db.close()
