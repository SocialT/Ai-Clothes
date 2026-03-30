from fastapi import APIRouter, HTTPException
from typing import List
from core.db import db
from schemas.style import StyleCreate, StyleUpdate, StylePublic

router = APIRouter()


@router.post("/", response_model=StylePublic)
async def create_style(style_data: StyleCreate):
    """Yeni stil oluştur (Admin)"""
    try:
        style = await db.style.create(data=style_data.dict())
        return style
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stil oluşturma hatası: {str(e)}")


@router.get("/", response_model=List[StylePublic])
async def list_styles(active_only: bool = True):
    """Aktif stilleri listele"""
    try:
        where_clause = {"isActive": True} if active_only else {}
        styles = await db.style.find_many(where=where_clause, order={"name": "asc"})
        return styles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stilller listelenirken hata: {str(e)}")


@router.get("/{style_id}", response_model=StylePublic)
async def get_style(style_id: int):
    """Tek bir stili getir"""
    try:
        style = await db.style.find_unique(where={"id": style_id})
        if not style:
            raise HTTPException(status_code=404, detail="Stil bulunamadı")
        return style
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stil getirme hatası: {str(e)}")


@router.put("/{style_id}", response_model=StylePublic)
async def update_style(style_id: int, style_data: StyleUpdate):
    """Stili güncelle (Admin)"""
    try:
        update_data = {k: v for k, v in style_data.dict().items() if v is not None}
        style = await db.style.update(where={"id": style_id}, data=update_data)
        return style
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stil güncelleme hatası: {str(e)}")


@router.delete("/{style_id}")
async def delete_style(style_id: int):
    """Stili sil (Admin)"""
    try:
        await db.style.delete(where={"id": style_id})
        return {"success": True, "message": "Stil silindi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stil silme hatası: {str(e)}")

