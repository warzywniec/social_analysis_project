import json
import xml.etree.ElementTree as ET
from app.models.headline import Headline
from app.models.site import Site
from app.db.session import SessionLocal

def import_headlines_from_json(filepath="app/export/headlines.json"):
    db = SessionLocal()
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        site_data = item["site"]
        site = db.query(Site).filter_by(category=site_data["category"], date=site_data["date"]).first()
        if not site:
            site = Site(category=site_data["category"], date=site_data["date"])
            db.add(site)
            db.commit()
            db.refresh(site)

        existing = db.query(Headline).filter_by(headline=item["headline"], site_id=site.id).first()
        if existing:
            continue

        headline = Headline(
            headline=item["headline"],
            date=item["date"],
            emotion=item["emotion"],
            site_id=site.id
        )
        db.add(headline)

    db.commit()
    db.close()


def import_headlines_from_xml(filepath="app/export/headlines.xml"):
    db = SessionLocal()
    tree = ET.parse(filepath)
    root = tree.getroot()

    for item in root.findall("Headline"):
        headline_text = item.find("headline").text
        date = item.find("date").text
        emotion = item.find("emotion").text
        site_elem = item.find("site")
        category = site_elem.find("category").text
        site_date = site_elem.find("date").text

        site = db.query(Site).filter_by(category=category, date=site_date).first()
        if not site:
            site = Site(category=category, date=site_date)
            db.add(site)
            db.commit()
            db.refresh(site)

        existing = db.query(Headline).filter_by(headline=headline_text, site_id=site.id).first()
        if existing:
            continue

        headline = Headline(
            headline=headline_text,
            date=date,
            emotion=emotion,
            site_id=site.id
        )
        db.add(headline)

    db.commit()
    db.close()
