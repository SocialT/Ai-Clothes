from fastapi import APIRouter, HTTPException
from typing import List
from core.db import db
from schemas.ambiance import AmbianceCreate, AmbianceUpdate, AmbiancePublic

router = APIRouter()


@router.post("/", response_model=AmbiancePublic)
async def create_ambiance(ambiance_data: AmbianceCreate):
    """Yeni ambiance oluştur (Admin)"""
    try:
        ambiance = await db.ambiance.create(data=ambiance_data.dict())
        return ambiance
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ambiance oluşturma hatası: {str(e)}")


@router.get("/", response_model=List[AmbiancePublic])
async def list_ambiances(active_only: bool = True):
    """Aktif ambianceleri listele"""
    try:
        where_clause = {"isActive": True} if active_only else {}
        ambiances = await db.ambiance.find_many(where=where_clause, order={"name": "asc"})
        return ambiances
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ambianceler listelenirken hata: {str(e)}")


@router.get("/{ambiance_id}", response_model=AmbiancePublic)
async def get_ambiance(ambiance_id: int):
    """Tek bir ambiance'i getir"""
    try:
        ambiance = await db.ambiance.find_unique(where={"id": ambiance_id})
        if not ambiance:
            raise HTTPException(status_code=404, detail="Ambiance bulunamadı")
        return ambiance
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ambiance getirme hatası: {str(e)}")


@router.put("/{ambiance_id}", response_model=AmbiancePublic)
async def update_ambiance(ambiance_id: int, ambiance_data: AmbianceUpdate):
    """Ambiance'i güncelle (Admin)"""
    try:
        update_data = {k: v for k, v in ambiance_data.dict().items() if v is not None}
        ambiance = await db.ambiance.update(where={"id": ambiance_id}, data=update_data)
        return ambiance
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ambiance güncelleme hatası: {str(e)}")


@router.delete("/{ambiance_id}")
async def delete_ambiance(ambiance_id: int):
    """Ambiance'i sil (Admin)"""
    try:
        await db.ambiance.delete(where={"id": ambiance_id})
        return {"success": True, "message": "Ambiance silindi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ambiance silme hatası: {str(e)}")

