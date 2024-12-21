from sqlalchemy import Column, Integer, String, ForeignKey, Date
from src.database.database import Base


class Country(Base):
    __tablename__ = "country"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)


class Tour(Base):
    __tablename__ = "tour"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    country_id = Column(Integer, ForeignKey("country.id"))
    hours = Column(Integer)
    price = Column(Integer)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    surname = Column(String)
    phone = Column(Integer)
    password = Column(String)
    power_level = Column(Integer, default=1)


class Ticket(Base):
    __tablename__ = "ticket"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tour_id = Column(Integer, ForeignKey("tour.id"))
    date_start = Column(Date)
    date_end = Column(Date)
    user_id = Column(Integer, ForeignKey("user.id"))

