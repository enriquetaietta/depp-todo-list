from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import datetime
from uuid import UUID
from backend.database.database import SessionLocal
from backend.database.models.todo.model import Todo, State, Priority
from backend.database.models.tag.model import Tag
from backend.database.models.todo_tag_relation.model import TodoTagRelation

router = APIRouter(prefix="/todo")

# Dipendenza per ottenere la sessione del database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modello Pydantic per la risposta GET
class TodoResponse(BaseModel):
    id: UUID
    title: str
    notes: Optional[str]
    state: State
    priority: Optional[Priority]
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True

@router.get("/", response_model=List[TodoResponse])
async def get_todos(
    state: Optional[str] = Query(None, description="Filter by state: ACTIVE, TODO, IN_PROGRESS, DONE"),
    title: Optional[str] = Query(None, description="Filter by title (like)"),
    priority: Optional[str] = Query(None, description="Filter by priority: low, medium, high"),
    sortby: Optional[str] = Query(None, description="Sort by: priority, created_at, state"),
    db: Session = Depends(get_db)
):
    # TODO -> Gestire i valori di state e priority secondo l'enum in input
    query = db.query(Todo).filter(Todo.deleted_at.is_(None))  # Filtra solo i record non cancellati

    # Filtro per lo stato
    if state == "ACTIVE":
        query = query.filter(Todo.state.in_([State.TODO, State.IN_PROGRESS]))
    elif state == "TODO":
        query = query.filter(Todo.state == State.TODO)
    elif state == "IN_PROGRESS":
        query = query.filter(Todo.state == State.IN_PROGRESS)
    elif state == "DONE":
        query = query.filter(Todo.state == State.DONE)

    # Filtro per il titolo
    if title:
        query = query.filter(Todo.title.like(f"%{title}%"))

    # Filtro per la priorità
    if priority:
        query = query.filter(Todo.priority == priority)

    # Ordinamento
    # TODO -> Di default le colonne datetime sono sortate in ordine descending
    # Da gestire possibilità di scelta asc/desc
    # TODO -> Gestire l'ordine di priority e state non in base ad ordine alfanumerico
    # ma in base ad un ordine enum
    if sortby == "priority":
        query = query.order_by(Todo.priority)
    elif sortby == "created_at":
        query = query.order_by(Todo.created_at.desc())
    elif sortby == "modified_at":
        query = query.order_by(Todo.modified_at.desc())
    elif sortby == "state":
        query = query.order_by(Todo.state.desc())

    todos = query.all()

    # TODO -> Da gestire la colonna TAG
    return todos

# Modello Pydantic per la richiesta POST
class TodoCreate(BaseModel):
    title: str = Field(..., max_length=200)
    notes: Optional[str] = Field(None) # TODO -> Gestire numero di parole non lunghezza caratteri
    priority: Optional[Priority] = Field(Priority.LOW)
    tags: List[str] = Field(default_factory=list)

    @validator('tags')
    def validate_tags(cls, v):
        if len(v) > 5:
            raise ValueError('Non puoi avere più di 5 tag')
        for tag in v:
            if len(tag) > 15:
                raise ValueError('I tag non possono superare i 15 caratteri')
        return v

@router.post("/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    try:
        # Crea il nuovo todo
        db_todo = Todo(
            title=todo.title,
            notes=todo.notes,
            priority=todo.priority,
            state=State.TODO # Default state sempre a TODO in creazione
        )
        db.add(db_todo)
        db.flush()  # Ottieni l'id del todo prima di committare
        print("INSERT TODO")
        # Gestisci i tag
        tag_ids = []
        for tag_code in todo.tags:
            # Verifica se il tag esiste già
            db_tag = db.query(Tag).filter(Tag.code == tag_code).first()
            if not db_tag:
                # Crea un nuovo tag
                db_tag = Tag(code=tag_code)
                db.add(db_tag)
                print("INSERT TAG")
                db.flush()  # Ottieni l'id del tag prima di committare
            tag_ids.append(db_tag.id)

        # Crea le relazioni tra todo e tag
        for tag_id in tag_ids:
            db_relation = TodoTagRelation(todo_id=db_todo.id, tag_id=tag_id)
            db.add(db_relation)
            print("INSERT TODOTAGRELATION")

        db.commit()
        db.refresh(db_todo)
        return db_todo
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )