from abc import ABC, abstractmethod
from typing import List, Optional
from app.entities import Memory

class MemoryRepository(ABC):
    @abstractmethod
    def add(self, memory: Memory) -> Memory:
        """Add a new book."""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Memory]:
        """Retrieve a memory by its ID."""
        pass

    @abstractmethod
    def get_all_memory(self, memory: Memory) -> List[Memory]:
        """Retrieve all memories from a user_id."""
        pass

    @abstractmethod
    def get_account_from_person(self, person_id: str) -> List[Account]:
        """Get all accounts from a person."""
        pass