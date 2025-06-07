from sqlalchemy import Column, Integer, String, Date, Text
from app.db.session import Base

class GDELTEntry(Base):
    __tablename__ = "gdelt_entries"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    title = Column(String, nullable=True)      # opcjonalnie z DocumentIdentifier lub z tytułu źródła
    source = Column(String, nullable=True)     # np. z SourceCommonName
    themes = Column(Text, nullable=True)       # dłuższe stringi – np. "TAX_EVASION;ECONOMY"
    locations = Column(Text, nullable=True)    # V2Locations
    organizations = Column(Text, nullable=True)  # V2Organizations
    