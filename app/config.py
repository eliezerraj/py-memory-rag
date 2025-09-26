import os
from dotenv import load_dotenv

load_dotenv(".env")

class Settings:
    def __init__(self):
        self.API_VERSION = os.getenv("API_VERSION")
        self.POD_NAME = os.getenv("POD_NAME")
        self.PORT = os.getenv("PORT")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASS = os.getenv("DB_PASS")

        self.DB_SCHEMA = os.getenv("DB_SCHEMA")
        self.DB_MAX_CONNECTION = os.getenv("DB_MAX_CONNECTION")
        self.DB_SSLMODE = os.getenv("DB_SSLMODE")

settings = Settings()
