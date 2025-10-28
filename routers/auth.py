from fastapi import APIRouter, HTTPException
from models import UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["Authentication"])

users_db = {}

@router.post("/register")
def register(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.email] = {"username": user.username, "password": user.password}
    return {"msg": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin):
    db_user = users_db.get(user.email)
    if not db_user or db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"msg": "Login successful", "username": db_user["username"]}