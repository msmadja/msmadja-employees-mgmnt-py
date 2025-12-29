from typing import Optional
from pydantic import BaseModel


class FindQuery(BaseModel):
    employee_code: Optional[str] = None
    skip: Optional[int] = 0
    limit: Optional[int] = 1000


class FindOneQuery(BaseModel):
    id: Optional[str] = None
    employee_code: Optional[str] = None


class InsertData(BaseModel):
    name: str
    employee_code: str
    salary: float


class DeleteQuery(BaseModel):
    id: Optional[str] = None
    employee_code: Optional[str] = None
