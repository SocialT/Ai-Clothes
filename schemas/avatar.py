from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AvatarCreate(BaseModel):
    name: str
    description: Optional[str] = None
    prompt: str


class AvatarUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    prompt: Optional[str] = None
    isActive: Optional[bool] = None


class AvatarPublic(BaseModel):
    id: int
    name: str
    description: Optional[str]
    prompt: str
    isActive: bool
    createdAt: datetime

    class Config:
        from_attributes = True

