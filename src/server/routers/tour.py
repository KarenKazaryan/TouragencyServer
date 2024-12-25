from fastapi import HTTPException, Depends
import fastapi
from sqlalchemy.orm import Session
from src.database.models import Tour
from src.database.pydantic_models import Tour as DbTour, ForId
from typing import List
from src.database.database import get_db

router = fastapi.APIRouter(prefix='/tour', tags=['Tour'])


@router.post("/create", response_model=DbTour)
async def create_tour(tour: DbTour, db: Session = Depends(get_db)) -> Tour:
    db_user = Tour(country_id=tour.country_id, hours=tour.hours, price=tour.price)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/read", response_model=List[DbTour])
async def get_tours(db: Session = Depends(get_db)) -> List[Tour]:
    db_users = db.query(Tour).all()
    return db_users


@router.get("/read/{id}", response_model=DbTour)
async def get_tour(id: int, db: Session = Depends(get_db)) -> Tour:
    db_user = db.query(Tour).filter(Tour.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="Tour not found")

    return db_user


@router.put("/update/{id}", response_model=DbTour)
async def update_tour(id: int, tour: DbTour, db: Session = Depends(get_db)) -> Tour:
    db_user = db.query(Tour).filter(Tour.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="Tour not found")

    db_user.country_id = tour.country_id
    db_user.hours = tour.hours
    db_user.price = tour.price

    db.commit()
    db.refresh(db_user)

    return db_user


@router.delete("/delete/{id}", response_model=ForId)
async def delete_tour(id: int, db: Session = Depends(get_db)):
    db_user = db.query(Tour).filter(Tour.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="Tour not found")

    db.delete(db_user)
    db.commit()

    return db_user
