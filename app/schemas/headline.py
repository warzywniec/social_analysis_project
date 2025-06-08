from pydantic import BaseModel

class HeadlineSchema(BaseModel):
    id: int
    headline: str
    date: str
    emotion: str

    class Config:
        orm_mode = True
