from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserSchema(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
