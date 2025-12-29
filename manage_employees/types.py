from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel


class Employee(BaseModel):
    name: str
    employee_code: str
    salary: float


class FullEmployee(Employee):
    id: str


class DeleteEmployee(BaseModel):
    id: Optional[str] = None
    employee_code: Optional[str] = None


class ManageEmployeesRequest(BaseModel):
    create: Optional[Employee] = None
    delete: Optional[DeleteEmployee] = None


ManageEmployeesResponse = bool


class QueryEmployeesFilters(BaseModel):
    employee_code: Optional[str] = None


class QueryEmployeesRequest(BaseModel):
    filters: Optional[QueryEmployeesFilters] = None
    skip: Optional[int] = 0
    limit: Optional[int] = 1000
    include_total: Optional[bool] = True


class QueryEmployeesResponse(BaseModel):
    data: List[FullEmployee]
    total: Optional[int] = None


class MngEmployees(ABC):

    @abstractmethod
    def manageEmployees(self, request: ManageEmployeesRequest) -> ManageEmployeesResponse:
        pass

    @abstractmethod
    def queryEmployees(self, request: QueryEmployeesRequest) -> QueryEmployeesResponse:
        pass
