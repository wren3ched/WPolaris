from fastapi import FastAPI
from database import Base, engine
from routes import auth, vault

app = FastAPI(title="Polaris WebApp")

Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/auth")
app.include_router(vault.router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a Polaris WebApp"}