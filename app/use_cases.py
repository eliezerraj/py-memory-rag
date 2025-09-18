import logging

from typing import List

from app.entities import Memory
from app.adapters.repositories import MemoryRepository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryService:
    def __init__(self, repository: MemoryRepository):
        self.repository = repository

    def get_memory(self, id: int) -> Memory:
        """Retrieve a Memory by ID."""
        return self.repository.get_by_id(id)
    
    def add_memory(self, user_id: str, message: str, vector_data: List[float]) -> Memory:
        """Add a new memory to the repository."""
        memory = Memory(id=0, user_id=user_id, message=message, vector_data=vector_data)  # ID will be assigned by DB
        return self.repository.add(memory)
    
    def get_all_memory(self, user_id: str) -> List[Memory]:
        """Retrieve all memories from a user_id."""
        memory = Memory(id=0, user_id=user_id)
        return self.repository.get_all_memory(memory)
        
    def get_cosine_sim(self, user_id: str, message: str, vector_data: List[float]) -> List[Memory]:
        """Retrieve a cosine similarity by a vector data."""
        logger.info("def get_cosine_sim")
        
        memory = Memory(id=0, user_id=user_id, message=message, vector_data=vector_data)
        return self.repository.get_cosine_sim(memory)