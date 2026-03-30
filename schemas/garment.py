from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class GarmentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    imageUrl: str
    category: Optional[str] = None


class GarmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None


class GarmentPublic(BaseModel):
    id: int
    userId: int
    name: str
    description: Optional[str]
    imageUrl: str
    category: Optional[str]
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

