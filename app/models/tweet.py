from sqlalchemy import Column, Integer, String, DateTime, Text
from app.db.session import Base

class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    source = Column(String, nullable=True)
    lang = Column(String(10), nullable=True)
    label = Column(String, default="unlabeled")  # jeśli kiedyś dodasz klasyfikację
    created_at = Column(DateTime, nullable=False)
