from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..database import get_database
from ..dependencies import get_current_user
from datetime import date

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate,
                       db: Session = Depends(get_database),
                       current_user: models.User = Depends(get_current_user)):
    return crud.create_user_transaction(db=db, transaction=transaction, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Transaction])
def read_transactions(skip: int = 0,
                      limit: int = 100,
                      db: Session = Depends(get_database),
                      current_user: models.User = Depends(get_current_user)):
    transactions = crud.get_transactions(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return transactions

@router.get("/report/monthly", response_model=dict)
def get_monthly_report(
        year: int = date.today().year,
        month: int = date.today().month,
        db: Session = Depends(get_database),
        current_user: models.User = Depends(get_current_user)):
    report = crud.get_monthly_report(db=db, user_id=current_user.id, year=year, month=month)
    return report
