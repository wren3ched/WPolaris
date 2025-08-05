from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt(text: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()

def decrypt(text: str, key: bytes) -> str:
    f= Fernet(key)
    return f.decrypt(text.encode()).decode()