from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine, Base
from .routers import users, transactions, categories, recurring_transactions

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Iniciando a aplicação...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tabelas criadas com sucesso.")

    yield

    print("Encerrando a aplicação...")


app = FastAPI(
    lifespan=lifespan,
    title="API de Controle Financeiro",
    description="Uma API completa para gerenciar suas finanças pessoais.",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(categories.router)
app.include_router(recurring_transactions.router)


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API de Controle Financeiro!"}