from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StyleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    prompt: str


class StyleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    prompt: Optional[str] = None
    isActive: Optional[bool] = None


class StylePublic(BaseModel):
    id: int
    name: str
    description: Optional[str]
    prompt: str
    isActive: bool
    createdAt: datetime

    class Config:
        from_attributes = True

