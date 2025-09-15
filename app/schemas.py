from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, TypeVar, List, Generic
from .models import TransactionType, FrequencyEnum

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    trans_type: TransactionType
    amount: float
    description: str

class TransactionCreate(TransactionBase):
    category_id: Optional[int] = None

class TransactionUpdate(BaseModel):
    trans_type: Optional[TransactionType] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    category_id: Optional[int] = None

class Transaction(TransactionBase):
    id: int
    user_id: int
    date: datetime
    category: Optional[Category] = None

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool = True
    # transactions: List[Transaction] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

DataT = TypeVar("DataT")
class Page(BaseModel, Generic[DataT]):
    items: List[DataT]
    total: int
    page: int
    size: int

class RecurringTransactionBase(BaseModel):
    description: str
    amount: float
    trans_type: TransactionType
    frequency: FrequencyEnum
    start_date: date
    end_date: Optional[date] = None
    category_id: Optional[int] = None
    day_of_month: Optional[int] = None
    day_of_week: Optional[int] = None


class RecurringTransactionCreate(RecurringTransactionBase):
    pass


class RecurringTransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    trans_type: Optional[TransactionType] = None
    frequency: Optional[FrequencyEnum] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    category_id: Optional[int] = None
    day_of_month: Optional[int] = None
    day_of_week: Optional[int] = None


class RecurringTransaction(RecurringTransactionBase):
    id: int
    user_id: int
    category: Optional[Category] = None

    class Config:
        orm_mode = True