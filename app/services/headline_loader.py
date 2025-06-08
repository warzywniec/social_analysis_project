import csv
import json
from app.models.headline import Headline
from app.models.site import Site
from app.db.session import SessionLocal

def load_headlines_from_csv(
    headlines_path: str = "app/data/classified_headlines.csv",
    sites_path: str = "app/data/sites_dataset.json"
):
    db = SessionLocal()

    with open(sites_path, "r", encoding="utf-8") as f:
        sites_data = json.load(f)

    with open(headlines_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for index, row in enumerate(reader):
            try:
                site_info = sites_data[index]
                category = site_info.get("category")
                date = site_info.get("date")

                site = (
                    db.query(Site)
                    .filter(Site.category == category, Site.date == date)
                    .first()
                )
                if not site:
                    site = Site(category=category, date=date)
                    db.add(site)
                    db.commit()
                    db.refresh(site)

                headline = Headline(
                    headline=row["headline"],
                    date=row["date"],
                    emotion=row["emotion"],
                    site_id=site.id
                )
                db.add(headline)

            except IndexError:
                print(f"Brak odpowiadającego site dla headline: {row}")
                continue

    db.commit()
    db.close()
