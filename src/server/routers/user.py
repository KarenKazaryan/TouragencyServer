from fastapi import HTTPException, Depends
import fastapi
from sqlalchemy.orm import Session
from src.database.models import User
from src.database.pydantic_models import User as DbUser, ForId
from typing import List
from src.database.database import get_db

router = fastapi.APIRouter(prefix='/user', tags=['User'])


@router.post("/create", response_model=DbUser)
async def create_user(user: DbUser, db: Session = Depends(get_db)) -> User:
    db_user = User(name=user.name, surname=user.surname, phone=user.phone, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login", response_model=DbUser)
async def login(phone: int, password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.phone == phone, User.password == password).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@router.get("/read", response_model=List[DbUser])
async def get_users(db: Session = Depends(get_db)) -> List[User]:
    db_users = db.query(User).all()
    return db_users


@router.get("/read/{id}", response_model=DbUser)
async def get_user(id: int, db: Session = Depends(get_db)) -> User:
    db_user = db.query(User).filter(User.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@router.put("/update/{id}", response_model=DbUser)
async def update_user(id: int, user: DbUser, db: Session = Depends(get_db)) -> User:
    db_user = db.query(User).filter(User.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.name = user.name
    db_user.surname = user.surname
    db_user.phone = user.phone
    db_user.password = user.password

    db.commit()
    db.refresh(db_user)

    return db_user


@router.delete("/delete/{id}", response_model=ForId)
async def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()

    return db_user
