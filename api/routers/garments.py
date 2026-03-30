from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import List, Optional
from core.db import db
from core.security import get_current_user
from core.storage import save_upload_file, get_file_url
from schemas.garment import GarmentCreate, GarmentUpdate, GarmentPublic

router = APIRouter()


@router.post("/", response_model=GarmentPublic)
async def create_garment(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    image: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    """Kıyafet yükle"""
    try:
        # Görseli kaydet
        file_path = await save_upload_file(image, subfolder="garments")
        image_url = get_file_url(file_path)
        
        # Veritabanına kaydet
        garment = await db.garment.create(
            data={
                "userId": current_user.id,
                "name": name,
                "description": description,
                "category": category,
                "imageUrl": image_url,
            }
        )
        return garment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kıyafet yükleme hatası: {str(e)}")


@router.get("/", response_model=List[GarmentPublic])
async def list_garments(
    category: Optional[str] = None,
    current_user=Depends(get_current_user)
):
    """Kullanıcının kıyafetlerini listele"""
    try:
        where_clause = {"userId": current_user.id}
        if category:
            where_clause["category"] = category
        
        garments = await db.garment.find_many(where=where_clause, order={"createdAt": "desc"})
        return garments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kıyafetler listelenirken hata: {str(e)}")


@router.get("/{garment_id}", response_model=GarmentPublic)
async def get_garment(garment_id: int, current_user=Depends(get_current_user)):
    """Tek bir kıyafeti getir"""
    try:
        garment = await db.garment.find_first(
            where={"id": garment_id, "userId": current_user.id}
        )
        if not garment:
            raise HTTPException(status_code=404, detail="Kıyafet bulunamadı")
        return garment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kıyafet getirme hatası: {str(e)}")


@router.put("/{garment_id}", response_model=GarmentPublic)
async def update_garment(
    garment_id: int,
    garment_data: GarmentUpdate,
    current_user=Depends(get_current_user)
):
    """Kıyafeti güncelle"""
    try:
        # Kıyafetin kullanıcıya ait olduğunu kontrol et
        existing = await db.garment.find_first(
            where={"id": garment_id, "userId": current_user.id}
        )
        if not existing:
            raise HTTPException(status_code=404, detail="Kıyafet bulunamadı")
        
        # Güncelle
        update_data = {k: v for k, v in garment_data.dict().items() if v is not None}
        garment = await db.garment.update(
            where={"id": garment_id},
            data=update_data
        )
        return garment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kıyafet güncelleme hatası: {str(e)}")


@router.delete("/{garment_id}")
async def delete_garment(garment_id: int, current_user=Depends(get_current_user)):
    """Kıyafeti sil"""
    try:
        # Kıyafetin kullanıcıya ait olduğunu kontrol et
        garment = await db.garment.find_first(
            where={"id": garment_id, "userId": current_user.id}
        )
        if not garment:
            raise HTTPException(status_code=404, detail="Kıyafet bulunamadı")
        
        # Sil (Cascade ile ilgili generation'lar da silinir)
        await db.garment.delete(where={"id": garment_id})
        return {"success": True, "message": "Kıyafet silindi"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kıyafet silme hatası: {str(e)}")

