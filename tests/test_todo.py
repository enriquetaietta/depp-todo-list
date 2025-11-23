import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database.database import Base, engine
from backend.database.models.todo.model import Todo, State
from backend.database.models.tag.model import Tag
from backend.database.models.todo_tag_relation.model import TodoTagRelation
import random
import string
# Log
import logging

# Configura il logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crea un client di test per l'app FastAPI
client = TestClient(app)

# Funzione per generare una stringa casuale
def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

# Fixture per creare e distruggere il database di test
@pytest.fixture(scope="module")
def setup_database():
    # Crea le tabelle
    Base.metadata.create_all(bind=engine)
    yield
    # Distruggi le tabelle
    Base.metadata.drop_all(bind=engine)

def test_get_todos(setup_database):
    # Test per verificare che l'API ritorni 200
    response = client.get("/api/v1/todo/")
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response content: {response.content}")
    assert response.status_code == 200

def test_create_todo_success(setup_database):
    # Test per verificare che la POST ritorni 200 con un titolo di 25 caratteri
    todo_data = {
        "title": random_string(25),
        "notes": "Test notes",
        "tags": ["tag1", "tag2"]
    }
    response = client.post("/api/v1/todo/", json=todo_data)
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response content: {response.content}")
    assert response.status_code == 200
    assert response.json()["title"] == todo_data["title"]

def test_create_todo_failure(setup_database):
    # Test per verificare che la POST ritorni un errore con un titolo di 201 caratteri
    todo_data = {
        "title": random_string(201),
        "notes": "Test notes",
        "tags": ["tag1", "tag2"]
    }
    response = client.post("/api/v1/todo/", json=todo_data)
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response content: {response.content}")
    assert response.status_code == 422  # Unprocessable Entity