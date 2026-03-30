from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


