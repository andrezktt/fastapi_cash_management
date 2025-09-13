from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .models import TransactionType

class TransactionBase(BaseModel):
    trans_type: TransactionType
    amount: float
    description: str

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    trans_type: Optional[TransactionType] = None
    amount: Optional[float] = None
    description: Optional[str] = None

class Transaction(TransactionBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True
    transactions: List[Transaction] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None