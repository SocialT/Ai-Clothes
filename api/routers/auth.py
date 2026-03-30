from fastapi import APIRouter, HTTPException, Depends
from core.db import db
from core.security import hash_password, verify_password, create_access_token, get_current_user
from schemas.auth import UserRegister, UserLogin, Token
from schemas.user import UserPublic


router = APIRouter()


@router.post("/register", response_model=Token)
async def register(payload: UserRegister):
    existing = await db.user.find_unique(where={"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayıtlı")

    user = await db.user.create(
        data={
            "name": payload.name,
            "email": payload.email,
            "passwordHash": hash_password(payload.password),
        }
    )
    token = create_access_token(subject=user.email)
    return Token(access_token=token)


@router.post("/login", response_model=Token)
async def login(payload: UserLogin):
    user = await db.user.find_unique(where={"email": payload.email})
    if not user or not verify_password(payload.password, user.passwordHash):
        raise HTTPException(status_code=401, detail="Geçersiz e-posta veya şifre")
    token = create_access_token(subject=user.email)
    return Token(access_token=token)


@router.get("/me", response_model=UserPublic)
async def me(current_user=Depends(get_current_user)):
    return current_user


