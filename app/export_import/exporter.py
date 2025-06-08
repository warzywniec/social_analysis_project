import json
import xml.etree.ElementTree as ET
from app.models.headline import Headline
from app.models.site import Site
from app.db.session import SessionLocal

def export_headlines_to_json(filepath="app/export/headlines.json"):
    db = SessionLocal()
    headlines = db.query(Headline).all()
    data = []
    for h in headlines:
        data.append({
            "headline": h.headline,
            "date": h.date,
            "emotion": h.emotion,
            "site": {
                "category": h.site.category if h.site else None,
                "date": h.site.date if h.site else None
            }
        })
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    db.close()


def export_headlines_to_xml(filepath="app/export/headlines.xml"):
    db = SessionLocal()
    headlines = db.query(Headline).all()
    root = ET.Element("Headlines")

    for h in headlines:
        item = ET.SubElement(root, "Headline")
        ET.SubElement(item, "headline").text = h.headline
        ET.SubElement(item, "date").text = h.date
        ET.SubElement(item, "emotion").text = h.emotion

        site_elem = ET.SubElement(item, "site")
        ET.SubElement(site_elem, "category").text = h.site.category if h.site else ""
        ET.SubElement(site_elem, "date").text = h.site.date if h.site else ""

    tree = ET.ElementTree(root)
    tree.write(filepath, encoding="utf-8", xml_declaration=True)
    db.close()
