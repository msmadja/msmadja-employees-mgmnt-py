import os
from functools import lru_cache
from pymongo import MongoClient


@lru_cache
def get_client():
    return MongoClient(os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017"))


def get_collection(name: str, db: str = "employee_mgmnt_db"):
    return get_client()[db][name]
