from sqlalchemy import Column, Integer, String
from database import Base  # IMPORTANTÍSSIMO!

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, index=True)