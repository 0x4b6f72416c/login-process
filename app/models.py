from email.headerregistry import UniqueSingleAddressHeader
from enum import unique
from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True)
    password = Column(String)
    