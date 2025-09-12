from sqlalchemy.orm import Session
from . import  models, schemas, auth
from sqlalchemy import func, extract

from .models import TransactionType


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_transaction(db: Session, transaction: schemas.TransactionCreate, user_id: int):
    db_transaction = models.Transaction(**transaction.model_dump(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (db.query(models.Transaction)
            .filter(models.Transaction.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all())

def get_monthly_report(db: Session, user_id: int, year: int, month: int):
    income = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == user_id,
        extract("year", models.Transaction.date) == year,
        extract("month", models.Transaction.date) == month,
        models.Transaction.trans_type == TransactionType.INCOME
    ).scalar() or 0.0

    expenses = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == user_id,
        extract("year", models.Transaction.date) == year,
        extract("month", models.Transaction.date) == month,
        models.Transaction.trans_type == TransactionType.EXPENSE
    ).scalar() or 0.0

    balance = income - expenses

    return {"income": income, "expenses": expenses, "balance": balance}