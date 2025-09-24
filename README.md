# API de Controle Financeiro  वित्त

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)
![Docker](https://img.shields.io/badge/Docker-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Uma API RESTful completa e assíncrona para gerenciamento de finanças pessoais, construída com uma stack de tecnologias moderna e escalável.

---

## 📋 Índice

- [Funcionalidades Principais](#-funcionalidades-principais)
- [✨ Stack de Tecnologias](#-stack-de-tecnologias)
- [🚀 Como Executar o Projeto](#-como-executar-o-projeto)
  - [Pré-requisitos](#pré-requisitos)
  - [Com Docker (Recomendado)](#com-docker-recomendado)
  - [Localmente (Alternativo)](#localmente-alternativo)
- [🔌 Uso da API (Endpoints)](#-uso-da-api-endpoints)

---

## 🎯 Funcionalidades Principais

* **Autenticação de Usuários:** Sistema completo de registro e login com tokens JWT.
* **Gerenciamento de Transações:** CRUD completo para receitas e despesas.
* **Categorias:** Usuários podem criar e associar categorias às suas transações.
* **Transações Recorrentes:** Sistema para gerenciar e executar automaticamente transações recorrentes (ex: salários, aluguéis).
* **Relatórios:** Endpoint para gerar relatórios mensais com total de receitas, despesas e saldo.
* **Busca Avançada:** Filtragem de transações por data, tipo e categoria, com sistema de paginação.
* **Arquitetura Assíncrona:** Alto desempenho e escalabilidade graças ao uso de `async/await` em toda a stack.
* **Migrações de Banco de Dados:** Schema do banco de dados versionado e gerenciado com Alembic.

---

## ✨ Stack de Tecnologias

* **Backend:** Python 3.12+
* **Framework:** FastAPI
* **Banco de Dados:** PostgreSQL
* **ORM:** SQLAlchemy 2.0 (com suporte `asyncio`)
* **Driver do Banco:** `asyncpg`
* **Validação de Dados:** Pydantic V2
* **Autenticação:** JWT (python-jose) + Passlib (para hashing de senhas)
* **Migrações:** Alembic
* **Testes:** Pytest
* **Ambiente e Pacotes:** `uv`
* **Containerização:** Docker & Docker Compose

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/products/docker-desktop/)
* [Docker Compose](https://docs.docker.com/compose/)

### Com Docker (Recomendado)

Este é o método mais simples e rápido para ter a aplicação rodando.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/andrezktt/fastapi_cash_management.git](https://github.com/andrezktt/fastapi_cash_management.git)
    cd fastapi_cash_management
    ```

2.  **Crie e configure o arquivo de ambiente:**
    Renomeie o arquivo `.env.example` (você pode criar um) para `.env` e preencha as variáveis. Para o Docker, é crucial que o `DATABASE_URL` aponte para o nome do serviço `db`.

    ```env
    # .env
    DATABASE_URL="postgresql+asyncpg://admin:password@db:5432/cash_management_db"
    TEST_DATABASE_URL="postgresql+asyncpg://admin:password@localhost:5432/cash_management_test_db"
    
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=password
    POSTGRES_DB=cash_management_db
    
    SECRET_KEY="seu-segredo-super-secreto-aqui"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

3.  **Suba os containers com Docker Compose:**
    Este comando irá construir a imagem da API, baixar a imagem do PostgreSQL e iniciar ambos os containers.
    ```bash
    docker-compose up --build
    ```
    Para rodar em segundo plano, adicione a flag `-d`.

4.  **Acesse a API:**
    * A API estará disponível em: `http://localhost:8000`
    * A documentação interativa (Swagger UI) em: `http://localhost:8000/docs`

### Localmente (Alternativo)

1.  **Clone o repositório** e entre na pasta.
2.  **Crie o ambiente virtual** e instale as dependências com `uv`:
    ```bash
    uv venv
    source .venv/bin/activate  # (ou .\.venv\Scripts\activate no Windows)
    uv pip sync
    ```
3.  **Configure o `.env`:** Use o mesmo arquivo `.env`, mas altere `DATABASE_URL` para apontar para `localhost`.
    ```env
    DATABASE_URL="postgresql+asyncpg://admin:password@localhost:5432/cash_management_db"
    ```
4.  **Execute as migrações** do banco de dados com Alembic:
    ```bash
    alembic upgrade head
    ```
5.  **Inicie o servidor** FastAPI com Uvicorn:
    ```bash
    uvicorn app.main:app --reload
    ```

---

## 🔌 Uso da API (Endpoints)

Após iniciar a aplicação, acesse a **[documentação interativa em http://localhost:8000/docs](http://localhost:8000/docs)** para ver todos os endpoints e testá-los diretamente pelo navegador.

### Principais Endpoints:

| Endpoint                       | Método HTTP    | Descrição                                    | Necessita Autenticação? |
|--------------------------------|----------------|----------------------------------------------|-------------------------|
| `/users/`                      | `POST`         | Registra um novo usuário.                    | Não                     |
| `/users/token`                 | `POST`         | Autentica um usuário e retorna um token JWT. | Não                     |
| `/users/me`                    | `GET`          | Retorna os dados do usuário logado.          | Sim                     |
| `/transactions/`               | `POST / GET`   | Cria ou lista as transações do usuário.      | Sim                     |
| `/transactions/{id}`           | `PUT / DELETE` | Atualiza ou deleta uma transação.            | Sim                     |
| `/transactions/report/monthly` | `GET`          | Gera o relatório financeiro do mês.          | Sim                     |
| `/categories/`                 | `POST / GET`   | Cria ou lista as categorias do usuário.      | Sim                     |
| `/recurring_transactions/`     | `POST / GET`   | Cria ou lista as regras de recorrência.      | Sim                     |

---
_Desenvolvido por [André Zicatti](https://github.com/andrezktt)._