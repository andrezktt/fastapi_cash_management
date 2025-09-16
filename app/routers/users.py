from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, auth, models
from .. database import get_database
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_database)):
    db_user = await crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Este email já está sendo utilizado.")
    return await crud.create_user(db=db, user=user)

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: AsyncSession = Depends(get_database), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.get_user_by_email(db=db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.User)
async def get_user_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.User)
async def update_user_me(user_in: schemas.UserUpdate,
                db: AsyncSession = Depends(get_database),
                current_user: models.User = Depends(get_current_user)):
    update_user = await crud.update_user(db, current_user, user_in)
    return update_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_me(db: AsyncSession = Depends(get_database),
                   current_user: models.User = Depends(get_current_user)):
    await crud.delete_user(db, current_user)
    return None