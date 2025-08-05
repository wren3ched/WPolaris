from fastapi import FastAPI
from database import Base, engine
from routes import auth, vault
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Polaris WebApp")

Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/auth")
app.include_router(vault.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://wpolaris-2.onrender.com"],  # o ["*"] para pruebas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Bienvenido a Polaris WebApp"}