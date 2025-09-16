import asyncio
import os
import sys
from datetime import date, datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, or_, extract

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base
from app.settings import settings
from app import models, schemas, crud

engine = create_async_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

async def process_daily_recurrences():
    async with SessionLocal() as db:
        today = date.today()
        print(f"Iniciando processamento de recorrências para {today.strftime('%Y-%m-%d')}...")
        rules_query = select(models.RecurringTransaction).filter(
            models.RecurringTransaction.start_date <= today,
            or_(
                models.RecurringTransaction.end_date >= today,
                models.RecurringTransaction.end_date.is_(None)
            )
        )
        result = await db.execute(rules_query)
        rules = result.scalars().all()

        for rule in rules:
            should_create = False
            if rule.frequency == models.FrequencyEnum.DAILY:
                should_create = True
            elif rule.frequency == models.FrequencyEnum.WEEKLY and rule.day_of_week == today.weekday():
                should_create = True
            elif rule.frequency == models.FrequencyEnum.MONTHLY and rule.day_of_month == today.day:
                should_create = True

            if should_create:
                existing_transaction_query = select(models.Transaction).filter(
                    models.Transaction.user_id == rule.user_id,
                    models.Transaction.description == rule.description,
                    models.Transaction.amount == rule.amount,
                    extract("year", models.Transaction.date) == today.year,
                    extract("month", models.Transaction.date) == today.month
                )
                result_existing = await db.execute(existing_transaction_query)
                existing_transaction = result_existing.scalars().first()

                if not existing_transaction:
                    print(f"Criando transação para a regra '{rule.description}' do usuário {rule.user_id}")
                    transaction_data = schemas.TransactionCreate(
                        trans_type=rule.trans_type,
                        amount=rule.amount,
                        description=rule.description,
                        category_id=rule.category_id,
                    )
                    await crud.create_user_transaction(db, transaction=transaction_data, user_id=rule.user_id)
                else:
                    print(f"Transação para a regra '{rule.description}' já existe este mês. Pulando.")

        print("Processamento finalizado.")

if __name__ == "__main__":
    asyncio.run(process_daily_recurrences())