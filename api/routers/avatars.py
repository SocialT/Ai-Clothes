from fastapi import APIRouter, HTTPException
from typing import List
from core.db import db
from schemas.avatar import AvatarCreate, AvatarUpdate, AvatarPublic

router = APIRouter()


@router.post("/", response_model=AvatarPublic)
async def create_avatar(avatar_data: AvatarCreate):
    """Yeni avatar oluştur (Admin)"""
    try:
        avatar = await db.avatar.create(data=avatar_data.dict())
        return avatar
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Avatar oluşturma hatası: {str(e)}")


@router.get("/", response_model=List[AvatarPublic])
async def list_avatars(active_only: bool = True):
    """Aktif avatarları listele"""
    try:
        where_clause = {"isActive": True} if active_only else {}
        avatars = await db.avatar.find_many(where=where_clause, order={"name": "asc"})
        return avatars
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Avatarlar listelenirken hata: {str(e)}")


@router.get("/{avatar_id}", response_model=AvatarPublic)
async def get_avatar(avatar_id: int):
    """Tek bir avatar'ı getir"""
    try:
        avatar = await db.avatar.find_unique(where={"id": avatar_id})
        if not avatar:
            raise HTTPException(status_code=404, detail="Avatar bulunamadı")
        return avatar
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Avatar getirme hatası: {str(e)}")


@router.put("/{avatar_id}", response_model=AvatarPublic)
async def update_avatar(avatar_id: int, avatar_data: AvatarUpdate):
    """Avatar'ı güncelle (Admin)"""
    try:
        update_data = {k: v for k, v in avatar_data.dict().items() if v is not None}
        avatar = await db.avatar.update(where={"id": avatar_id}, data=update_data)
        return avatar
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Avatar güncelleme hatası: {str(e)}")


@router.delete("/{avatar_id}")
async def delete_avatar(avatar_id: int):
    """Avatar'ı sil (Admin)"""
    try:
        await db.avatar.delete(where={"id": avatar_id})
        return {"success": True, "message": "Avatar silindi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Avatar silme hatası: {str(e)}")

