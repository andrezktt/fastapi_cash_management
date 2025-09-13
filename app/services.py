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