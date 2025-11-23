from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from uuid import UUID
from datetime import datetime
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
    id: Optional[UUID]
    title: str
    notes: Optional[str]
    state: State
    priority: Optional[Priority]
    tags: List[str]

    class Config:
        orm_mode = True

@router.get("/{id}", response_model=TodoResponse)
async def get_todo(
    id: UUID = Path(..., description="The ID of the todo to get"),
    db: Session = Depends(get_db)
):
    # Recupera il todo
    db_todo = db.query(Todo).filter(Todo.id == id, Todo.deleted_at.is_(None)).first()
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Recupera i tag associati al todo
    db_tags = db.query(Tag.code).join(TodoTagRelation, Tag.id == TodoTagRelation.tag_id).filter(
        TodoTagRelation.todo_id == id,
        TodoTagRelation.deleted_at.is_(None),
        Tag.deleted_at.is_(None)
    ).all()

    tags = [tag.code for tag in db_tags]

    return TodoResponse(
        id=db_todo.id,
        title=db_todo.title,
        notes=db_todo.notes,
        state=db_todo.state,
        priority=db_todo.priority,
        tags=tags
    )

# Modello Pydantic per la richiesta PUT
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = Field(None, max_length=150)
    state: Optional[State] = None
    priority: Optional[Priority] = None
    tags: Optional[List[str]] = Field(default_factory=list)

    @validator('tags')
    def validate_tags(cls, v):
        if v is not None:
            if len(v) > 5:
                raise ValueError('Non puoi avere più di 5 tag')
            for tag in v:
                if len(tag) > 15:
                    raise ValueError('I tag non possono superare i 15 caratteri')
        return v

@router.put("/{id}", response_model=TodoResponse)
async def update_todo(
    id: UUID = Path(..., description="The ID of the todo to update"),
    todo: TodoUpdate = None,
    db: Session = Depends(get_db)
):
    # Recupera il todo
    db_todo = db.query(Todo).filter(Todo.id == id, Todo.deleted_at.is_(None)).first()
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Aggiorna i campi del todo
    if todo.title is not None:
        db_todo.title = todo.title
    if todo.notes is not None:
        db_todo.notes = todo.notes
    if todo.priority is not None:
        db_todo.priority = todo.priority

    # Gestisci lo stato
    if todo.state is not None:
        if todo.state == State.DELETE:
            db_todo.deleted_at = datetime.utcnow()
        elif db_todo.state == State.TODO and todo.state == State.IN_PROGRESS:
            db_todo.state = State.IN_PROGRESS
        elif db_todo.state == State.IN_PROGRESS and todo.state == State.DONE:
            db_todo.state = State.DONE
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid state transition"
            )

    # Gestisci i tag
    if todo.tags is not None:
        # Cancella le relazioni esistenti
        db.query(TodoTagRelation).filter(
            TodoTagRelation.todo_id == id,
            TodoTagRelation.deleted_at.is_(None)
        ).update({"deleted_at": datetime.utcnow()})

        # Crea le nuove relazioni
        tag_ids = []
        for tag_code in todo.tags:
            # Verifica se il tag esiste già
            db_tag = db.query(Tag).filter(Tag.code == tag_code, Tag.deleted_at.is_(None)).first()
            if not db_tag:
                # Crea un nuovo tag
                db_tag = Tag(code=tag_code)
                db.add(db_tag)
                db.flush()
            tag_ids.append(db_tag.id)

        # Crea le nuove relazioni tra todo e tag
        for tag_id in tag_ids:
            db_relation = TodoTagRelation(todo_id=db_todo.id, tag_id=tag_id)
            db.add(db_relation)

    db.commit()
    db.refresh(db_todo)

    # Recupera i tag associati al todo
    db_tags = db.query(Tag.code).join(TodoTagRelation, Tag.id == TodoTagRelation.tag_id).filter(
        TodoTagRelation.todo_id == id,
        TodoTagRelation.deleted_at.is_(None),
        Tag.deleted_at.is_(None)
    ).all()

    tags = [tag.code for tag in db_tags]

    return TodoResponse(
        id=db_todo.id,
        title=db_todo.title,
        notes=db_todo.notes,
        state=db_todo.state,
        priority=db_todo.priority,
        tags=tags
    )