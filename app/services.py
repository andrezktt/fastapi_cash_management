from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import crud, models, schemas

def update_transaction(db: Session,
                       user: models.User,
                       transaction_id: int,
                       transaction_in: schemas.TransactionUpdate):
    db_transaction = crud.get_transactions(db, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found!")
    if db_transaction.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this transaction.")
    return crud.update_transaction(db, db_transaction, transaction_in)

def delete_transaction(db: Session,
                       user: models.User,
                       transaction_id: int):
    db_transaction = crud.get_transaction_by_id(db, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found!")
    if db_transaction.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this transaction.")
    crud.delete_transaction(db, db_transaction)
    return None

def update_category(db: Session,
                    user: models.User,
                    category_id: int,
                    category_in: schemas.CategoryUpdate):
    db_category = crud.get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found!")
    if db_category.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this category.")
    return crud.update_category(db, db_category, category_in)

def delete_category(db: Session,
                    user: models.User,
                    category_id: int):
    db_category = crud.get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found!")
    if db_category.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this category.")
    crud.delete_category(db, db_category)
    return None

def update_recurring_transaction(db: Session,
                                 user: models.User,
                                 recurring_id: int,
                                 recurring_transaction_in: schemas.RecurringTransactionUpdate):
    db_recurring_transaction = crud.get_recurring_transaction(db, recurring_id)
    if db_recurring_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurring Transaction not found!")
    if db_recurring_transaction.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this recurring transaction.")
    return crud.update_recurring_transaction(db, db_recurring_transaction, recurring_transaction_in)

def delete_recurring_transaction(db: Session,
                                 user: models.User,
                                 recurring_id: int):
    db_recurring_transaction = crud.get_recurring_transaction(db, recurring_id)
    if db_recurring_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurring Transaction not found!")
    if db_recurring_transaction.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this recurring transaction.")
    crud.delete_recurring_transaction(db, db_recurring_transaction)
    return None