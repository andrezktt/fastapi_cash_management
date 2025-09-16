from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from . import crud, models, schemas

async def create_transaction(
        db: AsyncSession,
        user: models.User,
        transaction_in: schemas.TransactionCreate
):
    if transaction_in.category_id is not None:
        category = await crud.get_category(db, category_id=transaction_in.category_id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {transaction_in.category_id} not found!"
            )
        if category.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to use this category."
            )
    return await crud.create_user_transaction(db, transaction_in, user.id)

async def update_transaction(
        db: AsyncSession,
        user: models.User,
        transaction_id: int,
        transaction_in: schemas.TransactionUpdate
):
    db_transaction = await crud.get_transaction_by_id(db, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found!")
    if db_transaction.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this transaction.")
    return await crud.update_transaction(db, db_transaction, transaction_in)

async def delete_transaction(
        db: AsyncSession,
        user: models.User,
        transaction_id: int
):
    db_transaction = await crud.get_transaction_by_id(db, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found!")
    if db_transaction.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this transaction.")
    await crud.delete_transaction(db, db_transaction)
    return None

async def update_category(
        db: AsyncSession,
        user: models.User,
        category_id: int,
        category_in: schemas.CategoryUpdate
):
    db_category = await crud.get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found!")
    if db_category.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this category.")
    return await crud.update_category(db, db_category, category_in)

async def delete_category(
        db: AsyncSession,
        user: models.User,
        category_id: int
):
    db_category = await crud.get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found!")
    if db_category.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this category.")
    await crud.delete_category(db, db_category)
    return None

async def update_recurring_transaction(
        db: AsyncSession,
        user: models.User,
        recurring_id: int,
        recurring_transaction_in: schemas.RecurringTransactionUpdate
):
    db_recurring_transaction = await crud.get_recurring_transaction(db, recurring_id)
    if db_recurring_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurring Transaction not found!")
    if db_recurring_transaction.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this recurring transaction.")
    return await crud.update_recurring_transaction(db, db_recurring_transaction, recurring_transaction_in)

async def delete_recurring_transaction(
        db: AsyncSession,
        user: models.User,
        recurring_id: int
):
    db_recurring_transaction = await crud.get_recurring_transaction(db, recurring_id)
    if db_recurring_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recurring Transaction not found!")
    if db_recurring_transaction.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this recurring transaction.")
    await crud.delete_recurring_transaction(db, db_recurring_transaction)
    return None