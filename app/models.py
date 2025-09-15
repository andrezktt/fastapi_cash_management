from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum, String, Date
from sqlalchemy.orm import relationship
from .database import Base
import enum
from datetime import datetime, UTC, date

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    transactions = relationship("Transaction", back_populates="owner", cascade='all, delete-orphan')
    categories = relationship("Category", back_populates="owner", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="categories")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trans_type = Column(Enum(TransactionType))
    amount = Column(Float, nullable=False)
    description = Column(String, index=True)
    date = Column(DateTime, default=datetime.now(UTC))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    owner = relationship("User", back_populates="transactions")
    category = relationship("Category")

class FrequencyEnum(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class RecurringTransaction(Base):
    __tablename__ = "recurring_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    description = Column(String, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    trans_type = Column(Enum(TransactionType), nullable=False)

    frequency = Column(Enum(FrequencyEnum), nullable=False)
    day_of_month = Column(Integer, nullable=True)
    day_of_week = Column(Integer, nullable=True)

    start_date = Column(Date, nullable=False, default=date.today())
    end_date = Column(Date, nullable=True)

    owner = relationship("User")
    category = relationship("Category")