from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.get("/", response_model=list[schemas.Contact])
def get_contacts(db: Session = Depends(get_db)):
    return db.query(models.Contact).order_by(models.Contact.name).all()


@router.post("/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    new_contact = models.Contact(
        name=contact.name,
        phone=contact.phone
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


@router.get("/{contact_id}", response_model=schemas.Contact)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
        return {"message": "Contato removido com sucesso!"}
    return {"error": "Contato não encontrado"}