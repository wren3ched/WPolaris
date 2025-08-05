from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from jose import jwt
from sqlalchemy.orm import Session
from database import SessionLocal
from models import VaultItem, User as DBUser
from crypto import encrypt, decrypt

router = APIRouter()

SECRET_KEY = "CLAVE"
ALGORITHM = "HS256"

class VaultEntry(BaseModel):
    service: str
    username: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(DBUser).filter(DBUser.username == username).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/vault")
def save_to_vault(entry: VaultEntry, current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)):
    key = current_user.encrypt(entry.password.encode())
    encrypted = encrypt(entry.username, key)

    vault_item = VaultItem(
        service=entry.service,
        encrypted_password=encrypted,
        user_id=current_user.id
    )
    db.add(vault_item)
    db.commit()
    return {"msg": f"Password for {entry.service} saved"}

@router.get("/vault")
def get_vault(current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(VaultItem).filter(VaultItem.user_id == current_user.id).all()
    result = []
    for item in items:
        key = current_user.encrypt(item.encrypted_password.encode())  # Or use stored key logic
        decrypted = decrypt(item.encrypted_password, key)
        result.append({"service": item.service, "password": decrypted})
    return {"vault": result}