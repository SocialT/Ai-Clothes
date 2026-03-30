from fastapi import APIRouter, HTTPException
from core.db import db
from schemas.user import UserCreate, UserPublic
from typing import List


router = APIRouter()


@router.post("/", response_model=UserPublic)
async def create_user(user_data: UserCreate):
    try:
        user = await db.user.create(
            data={
                "name": user_data.name,
                "email": user_data.email,
            }
        )
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kullanıcı oluşturma hatası: {str(e)}")


@router.get("/", response_model=List[UserPublic])
async def list_users():
    try:
        users = await db.user.find_many()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kullanıcılar listelenirken hata: {str(e)}")


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(user_id: int):
    try:
        user = await db.user.find_unique(where={"id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kullanıcı getirme hatası: {str(e)}")


