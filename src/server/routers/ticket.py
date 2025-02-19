from typing import List

import fastapi
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.database.models import Ticket
from src.database.pydantic_models import Ticket as DbTicket

router = fastapi.APIRouter(prefix='/ticket', tags=['Ticket'])


@router.post("/create", response_model=DbTicket)
async def create_tour(ticket: DbTicket, db: Session = Depends(get_db)) -> Ticket:
    db_user = Ticket(tour_id=ticket.tour_id, date_start=ticket.date_start, date_end=ticket.date_end,
                     user_id=ticket.user_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/read", response_model=List[DbTicket])
async def get_tickets(db: Session = Depends(get_db)) -> List[Ticket]:
    db_users = db.query(Ticket).all()
    return db_users


@router.get("/read/{id}", response_model=DbTicket)
async def get_ticket(id: int, db: Session = Depends(get_db)) -> Ticket:
    db_user = db.query(Ticket).filter(Ticket.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return db_user


@router.put("/update/{id}", response_model=DbTicket)
async def update_ticket(id: int, ticket: DbTicket, db: Session = Depends(get_db)) -> Ticket:
    db_user = db.query(Ticket).filter(Ticket.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db_user.tour_id = ticket.tour_id
    db_user.date_start = ticket.date_start
    db_user.date_end = ticket.date_end
    db_user.user_id = ticket.user_id

    db.commit()
    db.refresh(db_user)

    return db_user


@router.delete("/delete/{id}", response_model=bool)
async def delete_ticket(id: int, db: Session = Depends(get_db)):
    db_user = db.query(Ticket).filter(Ticket.id == id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(db_user)
    db.commit()

    return True
