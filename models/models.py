from datetime import datetime

from sqlalchemy import Column, TIMESTAMP, VARCHAR, Integer, Boolean, Text, ForeignKey, CHAR, BigInteger, SmallInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__: str = "users"

    id = Column(BigInteger, primary_key=True)
    lname = Column(Text, nullable=False)
    fname = Column(Text, nullable=False)
    mname = Column(Text, nullable=False)
    positions_id = Column(Integer, ForeignKey("positions.id", ondelete="NO ACTION"), nullable=False)


class Week(Base):
    __tablename__: str = "weeks"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="NO ACTION"), nullable=False)
    Monday = Column(Text, default=None)
    Tuesday = Column(Text, default=None)
    Wednesday = Column(Text, default=None)
    Thursday = Column(Text, default=None)
    Friday = Column(Text, default=None)
    Saturday = Column(Text, default=None)
    Sunday = Column(Text, default=None)


class Position(Base):
    __tablename__: str = "positions"

    id = Column(Integer, primary_key=True)
    name = Column(Text)


