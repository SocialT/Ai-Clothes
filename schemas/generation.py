from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class GenerationCreate(BaseModel):
    garmentId: Optional[int] = None
    originalImage: str
    style: Optional[str] = None
    ambiance: Optional[str] = None
    avatar: Optional[str] = None


class GenerationPublic(BaseModel):
    id: int
    userId: int
    garmentId: Optional[int]
    originalImage: str
    generatedImage: Optional[str]
    style: Optional[str]
    ambiance: Optional[str]
    avatar: Optional[str]
    prompt: Optional[str]
    status: str
    errorMessage: Optional[str]
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class GenerationStatus(BaseModel):
    id: int
    status: str
    generatedImage: Optional[str] = None
    errorMessage: Optional[str] = None

