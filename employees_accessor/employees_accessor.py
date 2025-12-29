from typing import Optional
from uuid import uuid4

from core import get_collection
from .types import FindQuery, FindOneQuery, InsertData, DeleteQuery

COLLECTION_NAME = "employees"

class EmployeesAccessor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def _collection(self):
        return get_collection(COLLECTION_NAME)

    def find(self, query: FindQuery = FindQuery()) -> list[dict]:
        q = {"employee_code": query.employee_code} if query.employee_code else {}
        return list(self._collection.find(q).skip(query.skip).limit(query.limit))

    def find_one(self, query: FindOneQuery) -> Optional[dict]:
        q = {}
        if query.id:
            q["_id"] = query.id
        if query.employee_code:
            q["employee_code"] = query.employee_code
        return self._collection.find_one(q)

    def insert(self, data: InsertData) -> str:
        doc = {
            "_id": str(uuid4()),
            "name": data.name,
            "employee_code": data.employee_code,
            "salary": data.salary,
        }
        self._collection.insert_one(doc)
        return doc["_id"]

    def update(self, id: str, **fields) -> bool:
        result = self._collection.update_one({"_id": id}, {"$set": fields})
        return result.modified_count > 0

    def delete(self, query: DeleteQuery) -> bool:
        q = {}
        if query.id:
            q["_id"] = query.id
        if query.employee_code:
            q["employee_code"] = query.employee_code
        if not q:
            return False
        result = self._collection.delete_one(q)
        return result.deleted_count > 0


accessor = EmployeesAccessor()
