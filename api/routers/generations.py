from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
from core.db import db
from core.security import get_current_user
from schemas.generation import GenerationCreate, GenerationPublic, GenerationStatus
from core.ai_service import generate_garment_image  # Bu servisi oluşturacağız

router = APIRouter()


@router.post("/", response_model=GenerationPublic)
async def create_generation(
    generation_data: GenerationCreate,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_user)
):
    """Yeni AI kıyafet değiştirme işlemi başlat"""
    try:
        # Garment kontrolü (eğer garmentId varsa)
        if generation_data.garmentId:
            garment = await db.garment.find_first(
                where={"id": generation_data.garmentId, "userId": current_user.id}
            )
            if not garment:
                raise HTTPException(status_code=404, detail="Kıyafet bulunamadı")
        
        # Generation kaydı oluştur
        generation = await db.generation.create(
            data={
                "userId": current_user.id,
                "garmentId": generation_data.garmentId,
                "originalImage": generation_data.originalImage,
                "style": generation_data.style,
                "ambiance": generation_data.ambiance,
                "avatar": generation_data.avatar,
                "status": "pending",
            }
        )
        
        # Background task olarak AI işlemini başlat
        background_tasks.add_task(
            process_generation,
            generation.id,
            generation_data.originalImage,
            generation_data.style,
            generation_data.ambiance,
            generation_data.avatar
        )
        
        return generation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"İşlem oluşturma hatası: {str(e)}")


async def process_generation(
    generation_id: int,
    original_image: str,
    style: Optional[str],
    ambiance: Optional[str],
    avatar: Optional[str]
):
    """AI işlemini arka planda gerçekleştir"""
    try:
        # Status'u processing'e güncelle
        await db.generation.update(
            where={"id": generation_id},
            data={"status": "processing"}
        )
        
        # AI servisini çağır (bu fonksiyonu oluşturacağız)
        result = await generate_garment_image(
            original_image=original_image,
            style=style,
            ambiance=ambiance,
            avatar=avatar
        )
        
        # Başarılı ise sonucu kaydet
        await db.generation.update(
            where={"id": generation_id},
            data={
                "status": "completed",
                "generatedImage": result["image_url"],
                "prompt": result.get("prompt"),
            }
        )
    except Exception as e:
        # Hata durumunda
        await db.generation.update(
            where={"id": generation_id},
            data={
                "status": "failed",
                "errorMessage": str(e)
            }
        )


@router.get("/", response_model=List[GenerationPublic])
async def list_generations(
    status: Optional[str] = None,
    current_user=Depends(get_current_user)
):
    """Kullanıcının AI işlemlerini listele"""
    try:
        where_clause = {"userId": current_user.id}
        if status:
            where_clause["status"] = status
        
        generations = await db.generation.find_many(
            where=where_clause,
            order={"createdAt": "desc"}
        )
        return generations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"İşlemler listelenirken hata: {str(e)}")


@router.get("/{generation_id}", response_model=GenerationPublic)
async def get_generation(generation_id: int, current_user=Depends(get_current_user)):
    """Tek bir AI işlemini getir"""
    try:
        generation = await db.generation.find_first(
            where={"id": generation_id, "userId": current_user.id}
        )
        if not generation:
            raise HTTPException(status_code=404, detail="İşlem bulunamadı")
        return generation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"İşlem getirme hatası: {str(e)}")


@router.get("/{generation_id}/status", response_model=GenerationStatus)
async def get_generation_status(generation_id: int, current_user=Depends(get_current_user)):
    """AI işleminin durumunu kontrol et"""
    try:
        generation = await db.generation.find_first(
            where={"id": generation_id, "userId": current_user.id}
        )
        if not generation:
            raise HTTPException(status_code=404, detail="İşlem bulunamadı")
        
        return GenerationStatus(
            id=generation.id,
            status=generation.status,
            generatedImage=generation.generatedImage,
            errorMessage=generation.errorMessage
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Durum kontrolü hatası: {str(e)}")

