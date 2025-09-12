from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users, transactions

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(transactions.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Controle Financeiro"}