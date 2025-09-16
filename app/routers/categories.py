from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import crud, schemas, models, services
from ..database import get_database
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate,
                    db: AsyncSession = Depends(get_database),
                    current_user: models.User = Depends(get_current_user)):
    return await crud.create_user_category(db, category, current_user.id)

@router.get("/", response_model=List[schemas.Category])
async def get_categories(skip: int = 0,
                   limit: int = 100,
                   db: AsyncSession = Depends(get_database),
                   current_user: models.User = Depends(get_current_user)):
    categories = await crud.get_categories_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return categories

@router.put("/{category_id}", response_model=schemas.Category)
async def update_category(category_id: int,
                    category_in: schemas.CategoryUpdate,
                    db: AsyncSession = Depends(get_database),
                    current_user: models.User = Depends(get_current_user)):
    return await services.update_category(db=db, user=current_user, category_id=category_id, category_in=category_in)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int,
                    db: AsyncSession = Depends(get_database),
                    current_user: models.User = Depends(get_current_user)):
    await services.delete_category(db=db, user=current_user, category_id=category_id)
    return None