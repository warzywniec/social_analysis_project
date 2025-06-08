from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    date = Column(String, nullable=False)

    headlines = relationship("Headline", back_populates="site")
