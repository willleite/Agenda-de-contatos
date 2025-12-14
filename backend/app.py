from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import SessionLocal, engine, Base
from models import Contact

# cria tabelas (simples)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agenda de Contatos")

# CORS - permitir frontend local (ajuste conforme necessário)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas
class ContactCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    notes: Optional[str] = None

class ContactRead(ContactCreate):
    id: int

    class Config:
        orm_mode = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contacts/", response_model=ContactRead)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(name=contact.name.strip(), phone=contact.phone.strip(), email=contact.email, notes=contact.notes)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.get("/contacts/", response_model=List[ContactRead])
def list_contacts(q: Optional[str] = Query(None, description="Pesquisa por nome (substring, case-insensitive)"), db: Session = Depends(get_db)):
    # pesquisa e ordena alfabeticamente por name (case-insensitive)
    query = db.query(Contact)
    if q:
        pattern = f"%{q.strip()}%"
        query = query.filter(func.lower(Contact.name).like(func.lower(pattern)))
    # ordenar alfabeticamente ignorando case
    query = query.order_by(func.lower(Contact.name))
    results = query.all()
    return results

@app.get("/contacts/{contact_id}", response_model=ContactRead)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return contact

@app.put("/contacts/{contact_id}", response_model=ContactRead)
def update_contact(contact_id: int, payload: ContactCreate, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    contact.name = payload.name.strip()
    contact.phone = payload.phone.strip()
    contact.email = payload.email
    contact.notes = payload.notes
    db.commit()
    db.refresh(contact)
    return contact

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    db.delete(contact)
    db.commit()
    return {"ok": True}