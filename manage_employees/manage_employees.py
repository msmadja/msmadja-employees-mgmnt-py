from employees_accessor import accessor, FindQuery, InsertData, DeleteQuery
from .types import (
    MngEmployees,
    ManageEmployeesRequest,
    ManageEmployeesResponse,
    QueryEmployeesRequest,
    QueryEmployeesResponse,
    FullEmployee,
)


class ManageEmployees(MngEmployees):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def manageEmployees(self, request: ManageEmployeesRequest) -> ManageEmployeesResponse:
        if request.create:
            accessor.insert(InsertData(
                name=request.create.name,
                employee_code=request.create.employee_code,
                salary=request.create.salary,
            ))
            return True

        if request.delete:
            return accessor.delete(DeleteQuery(
                id=request.delete.id,
                employee_code=request.delete.employee_code,
            ))

        return False

    def queryEmployees(self, request: QueryEmployeesRequest) -> QueryEmployeesResponse:
        query = FindQuery(
            employee_code=request.filters.employee_code if request.filters else None,
            skip=request.skip,
            limit=request.limit,
        )
        results = accessor.find(query)

        employees = [
            FullEmployee(
                id=doc["_id"],
                name=doc["name"],
                employee_code=doc["employee_code"],
                salary=doc["salary"],
            )
            for doc in results
        ]

        total = len(employees) if request.include_total else None
        return QueryEmployeesResponse(data=employees, total=total)


service: MngEmployees = ManageEmployees()
