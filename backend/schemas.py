from pydantic import BaseModel

class ContactBase(BaseModel):
    name: str
    phone: str

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class config:
        orm_mode = True