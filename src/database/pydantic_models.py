import datetime

from pydantic import BaseModel


class Country(BaseModel):
    id: int
    name: str


class CountryCreate(Country):
    pass


class CountryId(BaseModel):
    id: int


class Tour(BaseModel):
    id: int
    country_id: int
    hours: int
    price: int


class TourCreate(Tour):
    pass


class TourId(BaseModel):
    id: int


class User(BaseModel):
    id: int
    name: str
    surname: str
    phone: int
    password: str
    power_level: int

    class Config:
        orm_mode = True


class UserCreate(User):
    pass


class UserId(BaseModel):
    id: int


class Ticket(BaseModel):
    id: int
    tour_id: int
    date_start: datetime.date
    date_end: datetime.date
    user_id: int


class TicketCreate(Ticket):
    pass


class TicketId(BaseModel):
    id: int
