from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, Text, ForeignKey, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__: str = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    lname = Column(Text, nullable=False)
    fname = Column(Text, nullable=False)
    mname = Column(Text, nullable=False)
    positions_id = Column(Integer, ForeignKey("positions.id", ondelete="NO ACTION"))
    nickname = Column(Text, default=None)
    checked = Column(Boolean, default=False)


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    lname = Column(Text, nullable=False)
    fname = Column(Text, nullable=False)
    mname = Column(Text, nullable=False)


class Week(Base):
    __tablename__: str = "weeks"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="NO ACTION"), nullable=False)
    Monday = Column(Text, nullable=True)
    Tuesday = Column(Text, nullable=True)
    Wednesday = Column(Text, nullable=True)
    Thursday = Column(Text, nullable=True)
    Friday = Column(Text, nullable=True)
    Saturday = Column(Text, nullable=True)
    Sunday = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    handle = Column(Boolean, default=True)


class Position(Base):
    __tablename__: str = "positions"

    id = Column(Integer, primary_key=True)
    name = Column(Text)


