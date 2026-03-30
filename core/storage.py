import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
import aiofiles


UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
UPLOAD_DIR.mkdir(exist_ok=True)

IMAGES_DIR = UPLOAD_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)


async def save_upload_file(upload_file: UploadFile, subfolder: str = "") -> str:
    """
    Upload edilen dosyayı kaydeder ve URL döner
    """
    # Dosya uzantısını al
    file_ext = Path(upload_file.filename).suffix
    # Benzersiz dosya adı oluştur
    file_name = f"{uuid.uuid4()}{file_ext}"
    
    # Alt klasör oluştur
    target_dir = IMAGES_DIR / subfolder
    target_dir.mkdir(exist_ok=True)
    
    # Dosya yolunu oluştur
    file_path = target_dir / file_name
    
    # Dosyayı kaydet
    async with aiofiles.open(file_path, 'wb') as f:
        content = await upload_file.read()
        await f.write(content)
    
    # URL döndür (production'da CDN veya S3 URL'i olabilir)
    relative_path = f"uploads/images/{subfolder}/{file_name}" if subfolder else f"uploads/images/{file_name}"
    return relative_path


def get_file_url(file_path: str) -> str:
    """
    Dosya yolundan tam URL oluşturur
    """
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    return f"{base_url}/{file_path}"


async def delete_file(file_path: str) -> bool:
    """
    Dosyayı siler
    """
    try:
        full_path = Path(file_path)
        if full_path.exists():
            full_path.unlink()
            return True
        return False
    except Exception:
        return False

