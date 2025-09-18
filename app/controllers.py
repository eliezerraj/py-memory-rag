import logging

from app.config import settings
from fastapi import FastAPI, HTTPException, Depends

from app.entities import Memory
from app.use_cases import MemoryService
from app.adapters.postgres_repo import PostgresMemoryRepository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# ---------------------------------------------------------------
# methods memory
# ---------------------------------------------------------------
def get_memory_repository() -> PostgresMemoryRepository:
    """Dependency injection to get the memory repository."""

    connection_string = f"dbname={settings.DB_NAME} user={settings.DB_USER} password={settings.DB_PASS} host={settings.DB_HOST} port={settings.DB_PORT}"
    return PostgresMemoryRepository(connection_string)

@app.post("/memory", response_model=Memory)
def create_memory(memory: Memory, repository: PostgresMemoryRepository = Depends(get_memory_repository)):
    """Create a new memory."""

    return MemoryService(repository).add_memory(memory.user_id, memory.message, memory.vector_data)

@app.get("/memory/{memory_id}", response_model=Memory)
def read_memory(memory_id: int, repository: PostgresMemoryRepository = Depends(get_memory_repository)):
    """Retrieve a memory by ID."""
    
    memory = MemoryService(repository).get_memory(memory_id)
    if memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    
    return memory

@app.get("/memories/user/{user_id}", response_model=list[Memory])
def get_cosine_sim(user_id: str, repository: PostgresMemoryRepository = Depends(get_memory_repository)):
    """Retrieve all memories from a user_id."""

    return MemoryService(repository).get_all_memory(user_id)

@app.post("/memory_cosine_sim", response_model=list[Memory])
def get_cosine_sim(memory: Memory, repository: PostgresMemoryRepository = Depends(get_memory_repository)):
    """Retrieve a cosine similarity by a vector data."""
    logger.info("def get_cosine_sim")
    
    return MemoryService(repository).get_cosine_sim(memory.user_id, memory.message, memory.vector_data)