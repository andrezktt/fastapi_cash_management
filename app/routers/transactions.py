from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
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
async def create_transaction(
        transaction: schemas.TransactionCreate,
        db: AsyncSession = Depends(get_database),
        current_user: models.User = Depends(get_current_user)
):
    return await services.create_transaction(db, current_user, transaction)

@router.get("/", response_model=schemas.Page[schemas.Transaction])
async def read_transactions(
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        category_id: Optional[int] = None,
        trans_type: Optional[models.TransactionType] = None,
        page: int = 1,
        size: int = 20,
        db: AsyncSession = Depends(get_database),
        current_user: models.User = Depends(get_current_user)
):
    skip = (page - 1) * size
    result = await crud.get_transactions(
        db=db, user_id=current_user.id, skip=skip, limit=size,
        start_date=start_date, end_date=end_date, category_id=category_id, trans_type=trans_type
    )
    return schemas.Page(
        items=result["items"],
        total=result["total"],
        page=page,
        size=size
    )

@router.get("/report/monthly", response_model=dict)
async def get_monthly_report(
        year: int = date.today().year,
        month: int = date.today().month,
        db: AsyncSession = Depends(get_database),
        current_user: models.User = Depends(get_current_user)
):
    report = await crud.get_monthly_report(db=db, user_id=current_user.id, year=year, month=month)
    return report

@router.put("/{transaction_id}", response_model=schemas.Transaction)
async def update_transaction(
        transaction_id: int,
        transaction_in: schemas.TransactionUpdate,
        db: AsyncSession = Depends(get_database),
        current_user: models.User = Depends(get_current_user)
):
    return await services.update_transaction(db, current_user, transaction_id, transaction_in)

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
        transaction_id: int,
        db: AsyncSession = Depends(get_database),
        current_user: models.User = Depends(get_current_user)
):
    await services.delete_transaction(db, current_user, transaction_id)
    return None