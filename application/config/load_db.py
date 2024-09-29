import os
from dotenv import load_dotenv


def load_db():
    load_dotenv()  # This will load environment variables from .env
    DB_NAME = os.getenv("DB_NAME")  # Fetch DB_NAME from .env
    if DB_NAME:
        return DB_NAME
    else:
        raise ValueError("DB_NAME not found in environment variables")