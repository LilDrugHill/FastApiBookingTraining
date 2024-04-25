from sqlalchemy import JSON, Column, Integer, String
from app.database import Base


class Hotels(Base): # Для создания в бд необходимо init, revision, upgrade
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)


