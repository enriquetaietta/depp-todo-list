from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from uuid import UUID
from datetime import datetime
from backend.database.database import SessionLocal
from backend.database.models.tag.model import Tag

router = APIRouter(prefix="/tag")

# Dipendenza per ottenere la sessione del database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modello Pydantic per la risposta GET
class TagResponse(BaseModel):
    id: UUID
    code: str
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True

@router.get("/", response_model=List[TagResponse])
async def get_tags(db: Session = Depends(get_db)):
    # Recupera tutti i tag che non sono stati eliminati
    # TODO -> Gestire il recupero solo dei TAG che hanno effettivamenteuna relazione attiva
    # nella todo_tag_relations
    db_tags = db.query(Tag).filter(Tag.deleted_at.is_(None)).all()
    return db_tags

# Modello Pydantic per la richiesta POST
class TagCreate(BaseModel):
    code: str = Field(..., max_length=15)

@router.post("/", response_model=TagResponse)
async def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    try:
        # Verifica se il tag esiste già
        db_tag = db.query(Tag).filter(Tag.code == tag.code, Tag.deleted_at.is_(None)).first()
        if db_tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag already exists"
            )

        # Crea il nuovo tag
        db_tag = Tag(
            code=tag.code
        )
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        return db_tag
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )