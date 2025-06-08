from pydantic import BaseModel
from typing import Optional
from app.schemas.site import SiteSchema

class HeadlineSchema(BaseModel):
    id: int
    headline: str
    date: str
    emotion: str
    site: Optional[SiteSchema] = None

    class Config:
        orm_mode = True
