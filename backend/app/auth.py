from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import get_db
from .models import User
import os

SECRET_KEY = os.getenv("SECRET_KEY", "motoparts_secret_key_foarte_lunga_si_sigura_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 zile

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])

# ==================== SCHEMAS ====================
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    username: str

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "operator"

class UserRoleUpdate(BaseModel):
    role: str

# ==================== HELPERS ====================
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid sau expirat",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username)
    if user is None:
        raise credentials_exception
    return user

# ==================== LOGIN ====================
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Utilizator sau parolă greșită")

    if not user.approved and user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Contul tău nu a fost încă aprobat de administrator"
        )

    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "username": user.username
    }

# ==================== REGISTER ====================
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if len(user.username) < 3:
        raise HTTPException(status_code=400, detail="Username prea scurt (minim 3 caractere)")
    if len(user.password) < 4:
        raise HTTPException(status_code=400, detail="Parola prea scurtă (minim 4 caractere)")

    existing = get_user(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Utilizatorul există deja")

    db_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        role="operator",
        approved=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Cont creat. Așteaptă aprobarea administratorului."}

# ==================== USERS (ADMIN) ====================
@router.get("/users")
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Doar adminul poate vedea utilizatorii")
    
    users = db.query(User).all()
    return [
        {
            "id": str(u.id),
            "username": u.username,
            "role": u.role,
            "approved": u.approved
        } for u in users
    ]

@router.put("/users/{user_id}/approve")
def approve_user(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Doar adminul poate aproba")
    
    try:
        uid = UUID(user_id)
    except:
        raise HTTPException(status_code=400, detail="ID invalid")
    
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilizatorul nu există")
    
    user.approved = True
    db.commit()
    return {"message": f"Utilizatorul {user.username} a fost aprobat"}

@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: str,
    data: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Doar adminul poate schimba roluri")
    
    try:
        uid = UUID(user_id)
    except:
        raise HTTPException(status_code=400, detail="ID invalid")
    
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilizatorul nu există")
    
    if data.role not in ["admin", "operator"]:
        raise HTTPException(status_code=400, detail="Rol invalid. Folosește: admin sau operator")
    
    user.role = data.role
    db.commit()
    return {"message": f"Rolul lui {user.username} a fost schimbat în {data.role}"}

@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Doar adminul poate șterge")
    
    try:
        uid = UUID(user_id)
    except:
        raise HTTPException(status_code=400, detail="ID invalid")
    
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilizatorul nu există")
    
    if user.username == current_user.username:
        raise HTTPException(status_code=400, detail="Nu te poți șterge pe tine însuți")
    
    db.delete(user)
    db.commit()
    return {"message": "Utilizator șters"}
