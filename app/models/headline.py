from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Headline(Base):
    __tablename__ = "headlines"

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String, nullable=False)
    date = Column(String, nullable=False)
    emotion = Column(String, nullable=False)

    site_id = Column(Integer, ForeignKey("sites.id"))
    site = relationship("Site", back_populates="headlines")
