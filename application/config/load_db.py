import os
from dotenv import load_dotenv


def load_db():
    load_dotenv()  # This will load environment variables from .env
    DB_NAME = os.getenv("DB_NAME")  # Fetch DB_NAME from .env
    if DB_NAME:
        return DB_NAME
    else:
        raise ValueError("DB_NAME not found in environment variables")


def load_db_credentials():
    load_dotenv()  # This will load environment variables from .env
    DB_HOST = os.getenv("DB_HOST")  # Fetch DB_HOST from .env
    DB_USER = os.getenv("DB_USER")  # Fetch DB_USER from .env
    DB_PASSWORD = os.getenv("DB_PASSWORD")  # Fetch DB_PASS from .env
    return DB_HOST, DB_USER, DB_PASSWORD
