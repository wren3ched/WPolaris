from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta
from database import SessionLocal
from models import User as DBUser
from crypto import generate_key, encrypt, decrypt


router = APIRouter()

SECRET_KEY = "tu_clave_secreta"
ALGORITHM = "HS256"

class User(BaseModel):
    username: str
    password: str


db = SessionLocal()

@router.post("/register")
def register(user: User):
    if db.query(DBUser).filter(DBUser.username == user.username).first():
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    key = generate_key()
    encrypted_password = encrypt(user.password, key)

    new_user = DBUser(
        username=user.username,
        password=encrypted_password,
        encryption_key=key.decode()
    )
    db.add(new_user)
    db.commit()
    return {"msg": "Usuario registrado correctamente"}

@router.post("/login")
def login(user: User):
    db_user = db.query(DBUser).filter(DBUser.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # Recuperar la clave y descifrar la contraseña
    key = db_user.encryption_key.encode()
    decrypted_password = decrypt(db_user.password, key)

    if decrypted_password != user.password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = jwt.encode({
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token}

