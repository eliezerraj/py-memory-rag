import psycopg2
import logging

from psycopg2.extras import RealDictCursor
from typing import List, Optional

from app.adapters.repositories import MemoryRepository
from app.entities import Memory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

##       
class PostgresMemoryRepository(MemoryRepository):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def _connect(self):
        """Create a database connection to PostgreSQL."""
        try:
            logger.info("Database connection Successful !!!")
            return psycopg2.connect(self.connection_string)
        except Exception as e:
            logger.error("Database connection failed: %s", e)
            raise RuntimeError("Database connection failed") from e
        
    def get_by_id(self, id: int) -> Optional[Memory]:
        """Retrieve a Memory by its ID."""
        try:
            with self._connect() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("SELECT id, user_id, message, vector_data FROM memory WHERE id = %s", (id,))
                    row = cursor.fetchone()
                    if row:             
                        # Convert vector_data from string to list of floats
                        if isinstance(row["vector_data"], str):
                            cleaned = row["vector_data"].strip("[]")
                            row["vector_data"] = [float(x) for x in cleaned.split(",")]
                        return Memory(**row)
                    logger.warning("Memory with ID %s not found", id)
                    return None
        except Exception as e:
            logger.error("Error retrieving Memory with ID %s: %s", id, e)
            raise RuntimeError(f"Error retrieving Memory with ID {id}") from e
        
    def add(self, memory: Memory) -> Memory:
        """Add a new memory to the database."""
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    vector_str = "[" + ",".join(str(x) for x in memory.vector_data) + "]"
                    cursor.execute(
                        "INSERT INTO memory (user_id, message, vector_data) VALUES (%s, %s, %s) RETURNING id",
                        (memory.user_id, memory.message, vector_str)
                    )
                    memory.id = cursor.fetchone()[0]
                    conn.commit()
                    logger.info("Added memory with ID: %s", memory.id)
                    return memory
        except Exception as e:
            logger.error("Error adding memory: %s", e)
            raise RuntimeError("Error adding memory to the database") from e
        
    def get_all_memory(self, memory: Memory) -> List[Memory]:
        """Retrieve all memories from a user_id."""
        try:
            with self._connect() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("SELECT id, user_id, message, vector_data FROM memory WHERE user_id = %s", (memory.user_id,))

                    rows = cursor.fetchall()
                    memories = []
                    for row in rows:
                        if isinstance(row["vector_data"], str):
                            cleaned = row["vector_data"].strip("[]")
                            row["vector_data"] = [float(x) for x in cleaned.split(",")]
                        memories.append(Memory(**row))  
                    return memories
        except Exception as e:
            logger.error("Error retrieving Memory from user_id %s", memory.user_id, e)
            raise RuntimeError(f"Error retrieving Memory from user_id") from e
        
    def get_cosine_sim(self, memory: Memory) -> List[Memory]:
        """Retrieve a cosine similarity by a vector data.
            # -1: Vectors point in opposite directions (completely dissimilar)
            #  0: Vectors are perpendicular (no similarity)
            #  1: Vectors point in same direction (identical similarity)
        """
        logger.info("def get_cosine_sim")

        try:
            with self._connect() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    vector_str = "[" + ",".join(str(x) for x in memory.vector_data) + "]"

                    cursor.execute("SELECT id, user_id ,message, " \
                                    "1 - (vector_data <=> %s::vector) AS cosine_similarity, " \
                                    "ROW_NUMBER() OVER ( PARTITION BY message " \
                                    "ORDER BY 1 - (vector_data <=> %s::vector) desc ) as rn " \
                                    "FROM MEMORY " \
                                    "WHERE 1 - (vector_data <=> %s::vector) >= %s", (vector_str, vector_str, vector_str, 0.75))

                    rows = cursor.fetchall()
                    return [Memory(**row) for row in rows] 
        except Exception as e:
            logger.error("Error retrieving cousine similarity %s", 1, e)
            raise RuntimeError(f"Error retrieving cousine similarity") from e