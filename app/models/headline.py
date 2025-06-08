from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Headline(Base):
    __tablename__ = "headlines"

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String, nullable=False)
    date = Column(String, nullable=False)
    emotion = Column(String, nullable=False)
