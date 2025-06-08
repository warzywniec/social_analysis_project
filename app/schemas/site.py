from pydantic import BaseModel

class SiteSchema(BaseModel):
    id: int
    category: str
    date: str

    class Config:
        orm_mode = True
