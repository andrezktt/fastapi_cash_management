from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
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
async def create_new_recurring_transaction(
        recurring_transaction: schemas.RecurringTransactionCreate,
        db: AsyncSession = Depends(get_database),
        current_user: models.User = Depends(get_current_user)
):
    return await crud.create_recurring_transaction(db, recurring_transaction, current_user.id)

@router.get("/", response_model=List[schemas.RecurringTransaction])
async def read_user_recurring_transactions(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_database),
        current_user: models.User = Depends(get_current_user)
):
    return await crud.get_recurring_transactions_by_user(db, current_user.id, skip, limit)

@router.put("/{recurring_id}", response_model=schemas.RecurringTransaction)
async def update_recurring_transaction(
        recurring_id: int,
        recurring_transaction_in: schemas.RecurringTransactionUpdate,
        db: AsyncSession =Depends(get_database),
        current_user: models.User = Depends(get_current_user)
):
    return await services.update_recurring_transaction(db, current_user, recurring_id, recurring_transaction_in)

@router.delete("/{recurring_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recurring_transaction(
        recurring_id: int,
        db: AsyncSession = Depends(get_database),
        current_user: models.User = Depends(get_current_user)
):
    await services.delete_recurring_transaction(db, current_user, recurring_id)
    return None