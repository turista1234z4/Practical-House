from fastapi import FastAPI
from app.core.database import Base, engine


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Cria as tabelas no banco ao iniciar o backend
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "backend is running"}
