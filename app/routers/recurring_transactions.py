from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas, services
from ..database import get_database
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/recurring_transactions",
    tags=["recurring_transactions"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/", response_model=schemas.RecurringTransaction, status_code=status.HTTP_201_CREATED)
def create_new_recurring_transaction(recurring_transaction: schemas.RecurringTransactionCreate,
                                     db: Session = Depends(get_database),
                                     current_user: models.User = Depends(get_current_user)):
    return crud.create_recurring_transaction(db, recurring_transaction, current_user.id)

@router.get("/", response_model=List[schemas.RecurringTransaction])
def read_user_recurring_transactions(skip: int = 0, limit: int = 100,
                                     db: Session = Depends(get_database),
                                     current_user: models.User = Depends(get_current_user)):
    return crud.get_recurring_transactions_by_user(db, current_user.id, skip, limit)

@router.put("/{recurring_id}", response_model=schemas.RecurringTransaction)
def update_recurring_transaction(recurring_id: int, recurring_transaction_in: schemas.RecurringTransactionUpdate,
                                 db: Session =Depends(get_database), current_user: models.User = Depends(get_current_user)):
    return services.update_recurring_transaction(db, current_user, recurring_id, recurring_transaction_in)

@router.delete("/{recurring_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recurring_transaction(recurring_id: int, db: Session = Depends(get_database),
                                 current_user: models.User = Depends(get_current_user)):
    services.delete_recurring_transaction(db, current_user, recurring_id)
    return None