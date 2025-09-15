from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas, models, services
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

@router.get("/", response_model=schemas.Page[schemas.Transaction])
def read_transactions(start_date: Optional[date] = None, end_date: Optional[date] = None,
                      category_id: Optional[int] = None, trans_type: Optional[models.TransactionType] = None,
                      page: int = 1, size: int = 20, db: Session = Depends(get_database),
                      current_user: models.User = Depends(get_current_user)):
    skip = (page - 1) * size
    result = crud.get_transactions(
        db=db, user_id=current_user.id, skip=skip, limit=size,
        start_date=start_date, end_date=end_date, category_id=category_id, trans_type=trans_type
    )
    return schemas.Page(
        items=result["items"],
        total=result["total"],
        page=skip,
        size=size
    )

@router.get("/report/monthly", response_model=dict)
def get_monthly_report(
        year: int = date.today().year,
        month: int = date.today().month,
        db: Session = Depends(get_database),
        current_user: models.User = Depends(get_current_user)):
    report = crud.get_monthly_report(db=db, user_id=current_user.id, year=year, month=month)
    return report

@router.put("/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(transaction_id: int,
                       transaction_in: schemas.TransactionUpdate,
                       db: Session = Depends(get_database),
                       current_user: models.User = Depends(get_current_user)):
    return services.update_transaction(db, current_user, transaction_id, transaction_in)

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int,
                       db: Session = Depends(get_database),
                       current_user: models.User = Depends(get_current_user)):
    services.delete_transaction(db, current_user, transaction_id)
    return None