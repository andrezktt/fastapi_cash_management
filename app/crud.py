from sqlalchemy.orm import Session
from . import  models, schemas, auth
from sqlalchemy import func, extract

from .models import TransactionType

# User Methods
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: models.User, user_in: schemas.UserUpdate):
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        hashed_password = auth.get_password_hash(update_data["password"])
        update_data["password"] = hashed_password
        update_data["hashed_password"] = update_data.pop("password")
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: models.User):
    db.delete(db_user)
    db.commit()
    return db_user

# Transaction Methods
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

def get_transaction_by_id(db: Session, transaction_id: int):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

def update_transaction(db: Session, db_transaction: models.Transaction, transaction_in: schemas.TransactionUpdate):
    update_data = transaction_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_transaction, key, value)

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, db_transaction: models.Transaction):
    db.delete(db_transaction)
    db.commit()
    return db_transaction

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

# Category Methods
def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Category).filter(models.Category.user_id == user_id).offset(skip).limit(limit).all()

def create_user_category(db: Session, category: schemas.CategoryCreate, user_id: int):
    db_category = models.Category(**category.model_dump(), user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category