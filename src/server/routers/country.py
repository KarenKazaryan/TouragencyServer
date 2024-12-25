from fastapi import HTTPException, Depends
import fastapi
from sqlalchemy.orm import Session
from src.database.models import Country
from src.database.pydantic_models import Country as DbCountry, ForId
from typing import List
from src.database.database import get_db

router = fastapi.APIRouter(prefix='/country', tags=['Country'])


@router.post("/create", response_model=DbCountry)
async def create_country(country: DbCountry, db: Session = Depends(get_db)) -> Country:
    db_user = Country(name=country.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/read", response_model=List[DbCountry])
async def get_countryes(db: Session = Depends(get_db)) -> List[Country]:
    db_users = db.query(Country).all()
    return db_users


@router.get("/read/{id}", response_model=DbCountry)
async def get_country(id: int, db: Session = Depends(get_db)) -> Country:
    db_user = db.query(Country).filter(Country.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="Country not found")

    return db_user


@router.put("/update/{id}", response_model=DbCountry)
async def update_country(id: int, country: DbCountry, db: Session = Depends(get_db)) -> Country:
    db_user = db.query(Country).filter(Country.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="Country not found")

    db_user.name = country.name

    db.commit()
    db.refresh(db_user)

    return db_user


@router.delete("/delete/{id}", response_model=ForId)
async def delete_country(id: int, db: Session = Depends(get_db)):
    db_user = db.query(Country).filter(Country.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="Country not found")

    db.delete(db_user)
    db.commit()

    return db_user
