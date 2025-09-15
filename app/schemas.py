from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .models import TransactionType

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