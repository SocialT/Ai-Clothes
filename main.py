from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.db import db
from api.routers import auth, users, garments, generations, styles, ambiances, avatars

app = FastAPI(
    title="AI Clothes API",
    description="AI ile kıyafet değiştirme uygulaması API",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    try:
        await db.connect()
        print("✅ Veritabanı bağlantısı başarılı!")
    except Exception as e:
        print(f"❌ Veritabanı bağlantı hatası: {e}")

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@app.get("/")
async def root():
    return {"message": "AI Clothes API", "status": "running", "version": "1.0.0"}

# Static files (uploaded images)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(garments.router, prefix="/garments", tags=["Garments"])
app.include_router(generations.router, prefix="/generations", tags=["AI Generations"])
app.include_router(styles.router, prefix="/styles", tags=["Styles"])
app.include_router(ambiances.router, prefix="/ambiances", tags=["Ambiances"])
app.include_router(avatars.router, prefix="/avatars", tags=["Avatars"])
