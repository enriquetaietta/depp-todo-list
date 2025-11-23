from fastapi import FastAPI
from backend.database.database import init_db
from backend.api.v1.todo.todo import router as todo_router
from backend.api.v1.todo.id.id import router as todo_id_router
from backend.api.v1.tag.tag import router as tag_router
from backend.middleware.cors import add_middleware

app = FastAPI()

# Aggiungi il middleware
add_middleware(app)

@app.on_event("startup")
async def startup_event():
    init_db()

# Router endpoint v1
app.include_router(todo_router, prefix="/api/v1", tags=["todo"])
app.include_router(todo_id_router, prefix="/api/v1", tags=["todo_id"])
app.include_router(tag_router, prefix="/api/v1", tags=["tag"])
