import pandas as pd
import requests, zipfile, io
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, timedelta
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

# Zakres dat
start_date = datetime(2024, 11, 1)
end_date = datetime(2024, 12, 31)

current_date = start_date

while current_date <= end_date:
    date_str = current_date.strftime("%Y%m%d")
    url = f"http://data.gdeltproject.org/gdeltv2/{date_str}.gkg.csv.zip"
    print(f"Pobieranie: {url}")

    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print(f"Brak danych dla {date_str}")
            current_date += timedelta(days=1)
            continue

        z = zipfile.ZipFile(io.BytesIO(r.content))
        csv_filename = z.namelist()[0]

        df = pd.read_csv(z.open(csv_filename), sep='\t', header=None, low_memory=False)

        df.columns = ["GKGRECORDID", "DATE", "SourceCollectionIdentifier", "SourceCommonName",
                      "DocumentIdentifier", "Counts", "V2Counts", "Themes", "V2Themes",
                      "Locations", "V2Locations", "Persons", "V2Persons", "Organizations",
                      "V2Organizations", "V2Tone", "Dates", "GCAM", "SharingImage", "RelatedImages",
                      "SocialImageEmbeds", "SocialVideoEmbeds", "Quotations", "AllNames",
                      "Amounts", "TranslationInfo", "Extras"]

        for _, row in df.head(100).iterrows():  # ograniczamy do 100 wpisów dziennie
            try:
                entry_date = datetime.strptime(str(row["DATE"]), "%Y%m%d")
            except Exception:
                entry_date = current_date

            entry = GDELTEntry(
                date=entry_date,
                themes=row.get("V2Themes", ""),
                locations=row.get("V2Locations", ""),
                organizations=row.get("V2Organizations", "")
            )
            session.add(entry)

        print(f"Wczytano dane z {date_str}")
        session.commit()

    except Exception as e:
        print(f"Błąd przy {date_str}: {e}")

    current_date += timedelta(days=1)

print("Zakończono wczytywanie danych GDELT.")

# import pandas as pd
# import requests, zipfile, io
# from sqlalchemy import Column, Integer, String, DateTime, Text
# from sqlalchemy.orm import sessionmaker
# from datetime import datetime
# from app.db.session import engine, SessionLocal, Base
# from app.models.gdelt import GDELTEntr

# class GDELTEntry(Base):
#     __tablename__ = "gdelt_entries"
#     id = Column(Integer, primary_key=True)
#     date = Column(DateTime)
#     themes = Column(Text)
#     locations = Column(Text)
#     organizations = Column(Text)

# # DB setup
# # SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
# session = SessionLocal()

# # Download CSV from GDELT
# url = "http://data.gdeltproject.org/gdeltv2/20250530.gkg.csv.zip"
# r = requests.get(url)
# z = zipfile.ZipFile(io.BytesIO(r.content))
# csv_filename = z.namelist()[0]
# df = pd.read_csv(z.open(csv_filename), sep='\t', header=None, low_memory=False)

# # Map columns based on GDELT doc
# df.columns = ["GKGRECORDID", "DATE", "SourceCollectionIdentifier", "SourceCommonName",
#               "DocumentIdentifier", "Counts", "V2Counts", "Themes", "V2Themes",
#               "Locations", "V2Locations", "Persons", "V2Persons", "Organizations",
#               "V2Organizations", "V2Tone", "Dates", "GCAM", "SharingImage", "RelatedImages",
#               "SocialImageEmbeds", "SocialVideoEmbeds", "Quotations", "AllNames",
#               "Amounts", "TranslationInfo", "Extras"]

# # Insert small sample
# for _, row in df.head(100).iterrows():
#     entry = GDELTEntry(
#         date=datetime.strptime(str(row["DATE"]), "%Y%m%d"),
#         themes=row["V2Themes"],
#         locations=row["V2Locations"],
#         organizations=row["V2Organizations"]
#     )
#     session.add(entry)

# session.commit()
# print("Wczytano dane GDELT.")
