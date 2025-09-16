from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from sqlalchemy.orm import selectinload
from datetime import datetime, date, timezone, UTC
from . import  models, schemas, auth
from typing import Optional

# User Methods
async def get_user_by_email(
        db: AsyncSession,
        email: str
):
    query = select(models.User).filter(models.User.email == email)
    result = await db.execute(query)
    return result.scalars().first()

async def create_user(
        db: AsyncSession,
        user: schemas.UserCreate
):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(
        db: AsyncSession,
        db_user: models.User,
        user_in: schemas.UserUpdate
):
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        hashed_password = auth.get_password_hash(update_data["password"])
        update_data["password"] = hashed_password
        update_data["hashed_password"] = update_data.pop("password")
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(
        db: AsyncSession,
        db_user: models.User
):
    await db.delete(db_user)
    await db.commit()
    return db_user

# Transaction Methods
async def get_transaction_by_id(
        db: AsyncSession,
        transaction_id: int
):
    query = (select(models.Transaction)
             .options(selectinload(models.Transaction.category))
             .filter(models.Transaction.id == transaction_id))
    result = await db.execute(query)
    return result.scalars().first()

async def get_transactions(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        category_id: Optional[int] = None,
        trans_type: Optional[models.TransactionType] = None
):
    query = (select(models.Transaction)
             .options(selectinload(models.Transaction.category))
             .filter(models.Transaction.user_id == user_id))

    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        end_datetime = datetime.combine(end_date, datetime.max.time())
        query = query.filter(models.Transaction.date <= end_datetime)
    if category_id is not None:
        query = query.filter(models.Transaction.category_id == category_id)
    if trans_type:
        query = query.filter(models.Transaction.trans_type == trans_type)

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    items_query = query.order_by(models.Transaction.date.desc()).offset(skip).limit(limit)
    items_result = await db.execute(items_query)
    items = items_result.scalars().all()

    return {"items": items, "total": total}

async def create_user_transaction(
        db: AsyncSession,
        transaction: schemas.TransactionCreate,
        user_id: int
):
    db_transaction = models.Transaction(**transaction.model_dump(), user_id=user_id)
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return await get_transaction_by_id(db, db_transaction.id)

async def update_transaction(
        db: AsyncSession,
        db_transaction: models.Transaction,
        transaction_in: schemas.TransactionUpdate
):
    update_data = transaction_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_transaction, key, value)
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return await get_transaction_by_id(db, db_transaction.id)

async def delete_transaction(
        db: AsyncSession,
        db_transaction: models.Transaction
):
    await db.delete(db_transaction)
    await db.commit()
    return db_transaction

async def get_monthly_report(
        db: AsyncSession,
        user_id: int,
        year: int,
        month: int
):
    base_query = select(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == user_id,
        extract("year", models.Transaction.date) == year,
        extract("month", models.Transaction.date) == month,
    )

    income_query = base_query.filter(models.Transaction.trans_type == models.TransactionType.INCOME)
    income_result = await db.execute(income_query)
    income = income_result.scalar_one_or_none() or 0.0

    expenses_query = base_query.filter(models.Transaction.trans_type == models.TransactionType.EXPENSE)
    expenses_result = await db.execute(expenses_query)
    expenses = expenses_result.scalar_one_or_none() or 0.0

    balance = income - expenses
    return {"income": income, "expenses": expenses, "balance": balance}

# Category Methods
async def get_category(
        db: AsyncSession,
        category_id: int
):
    query = select(models.Category).filter(models.Category.id == category_id)
    result = await db.execute(query)
    return result.scalars().first()

async def get_categories_by_user(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100
):
    query = select(models.Category).filter(models.Category.user_id == user_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def create_user_category(
        db: AsyncSession,
        category: schemas.CategoryCreate,
        user_id: int
):
    db_category = models.Category(**category.model_dump(), user_id=user_id)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def update_category(
        db: AsyncSession,
        db_category: models.Category,
        category_in: schemas.CategoryUpdate
):
    update_data = category_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def delete_category(
        db: AsyncSession,
        db_category: models.Category
):
    await db.delete(db_category)
    await db.commit()
    return db_category

# Recurring Transactions Methods
async def get_recurring_transaction(
        db: AsyncSession,
        recurring_transaction_id: int
):
    query = (select(models.RecurringTransaction)
             .options(selectinload(models.RecurringTransaction.category))
             .filter(models.RecurringTransaction.id == recurring_transaction_id))
    result = await db.execute(query)
    return result.scalars().first()

async def get_recurring_transactions_by_user(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100
):
    query = (select(models.RecurringTransaction)
             .options(selectinload(models.RecurringTransaction.category))
             .filter(models.RecurringTransaction.user_id == user_id).offset(skip).limit(limit))
    result = await db.execute(query)
    return result.scalars().all()

async def create_recurring_transaction(
        db: AsyncSession,
        recurring_transaction: schemas.RecurringTransactionCreate,
        user_id: int
):
    db_recurring_transaction = models.RecurringTransaction(**recurring_transaction.model_dump(), user_id=user_id)
    db.add(db_recurring_transaction)
    await db.commit()
    await db.refresh(db_recurring_transaction)
    return await get_recurring_transaction(db, db_recurring_transaction.id)

async def update_recurring_transaction(
        db: AsyncSession,
        db_recurring_transaction: models.RecurringTransaction,
        recurring_transaction_in: schemas.RecurringTransactionUpdate
):
    update_data = recurring_transaction_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_recurring_transaction, key, value)
    db.add(db_recurring_transaction)
    await db.commit()
    await db.refresh(db_recurring_transaction)
    return await get_recurring_transaction(db, db_recurring_transaction.id)

async def delete_recurring_transaction(
        db: AsyncSession,
        db_recurring_transaction: models.RecurringTransaction):
    await db.delete(db_recurring_transaction)
    await db.commit()
    return db_recurring_transaction