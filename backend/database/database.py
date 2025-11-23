import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Base comune
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Importa i modelli delle tabelle
from backend.database.models.tag.model import Tag
from backend.database.models.todo.model import Todo
from backend.database.models.todo_tag_relation.model import TodoTagRelation

# Nome del database
DATABASE_NAME = "depp_todo_list.db"

# Verifica se il database esiste già
if not os.path.exists(DATABASE_NAME):
    # Crea il database
    engine = create_engine(f"sqlite:///{DATABASE_NAME}")

    # Crea le tabelle
    Base.metadata.create_all(engine)

    # Chiudi la connessione
    engine.dispose()

# Configura la connessione al database
engine = create_engine(f"sqlite:///{DATABASE_NAME}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Funzione per inizializzare il database
def init_db():
    # Verifica se il database esiste già
    if not os.path.exists(DATABASE_NAME):
        # Crea il database
        engine = create_engine(f"sqlite:///{DATABASE_NAME}")
        Base = declarative_base()

        # Crea le tabelle
        Base.metadata.create_all(engine)

        # Chiudi la connessione
        engine.dispose()