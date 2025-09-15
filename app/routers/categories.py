from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..database import get_database
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate,
                    db: Session = Depends(get_database),
                    current_user: models.User = Depends(get_current_user)):
    return crud.create_user_category(db, category, current_user.id)

@router.get("/", response_model=List[schemas.Category])
def get_categories(skip: int = 0,
                   limit: int = 100,
                   db: Session = Depends(get_database),
                   current_user: models.User = Depends(get_current_user)):
    categories = crud.get_categories_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return categories