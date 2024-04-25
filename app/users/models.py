from sqlalchemy import JSON, Column, Integer, String
from app.database import Base


class Users(Base): # Для создания в бд необходимо init, revision, upgrade
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
