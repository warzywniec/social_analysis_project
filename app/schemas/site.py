from pydantic import BaseModel
from typing import Optional

class SiteSchema(BaseModel):
    id: int
    category: str
    date: str

    class Config:
        orm_mode = True
