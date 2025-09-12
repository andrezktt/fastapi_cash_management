# 💰 API de Controle Financeiro

API RESTful desenvolvida em **Python + FastAPI** para gerenciamento de receitas e despesas, com relatórios mensais.

---

## 🚀 Funcionalidades
- Registro e login de usuários
- Autenticação JWT
- CRUD de receitas e despesas
- Relatórios mensais de saldo
- Documentação automática com Swagger (OpenAPI)

---

## 🛠️ Tecnologias
- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL / SQLite
- JWT
- Pytest

---

## 📂 Estrutura do Projeto
```
    app/
├── main.py
├── models/
├── routes/
├── services/
└── database.py
tests/
```

---

## ⚡ Como executar
```bash
# Clone o repositório
git clone https://github.com/seuusuario/finance-api.git
cd finance-api

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt

# Rode a API
uvicorn app.main:app --reload
```

API em: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs

## ✅ Testes
```bash
pytest
```

---

## 📜 Licença
MIT