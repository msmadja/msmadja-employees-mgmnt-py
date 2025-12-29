from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional

from core import api_exception_handler
from manage_employees import service
from manage_employees.types import (
    Employee,
    DeleteEmployee,
    ManageEmployeesRequest,
    QueryEmployeesRequest,
    QueryEmployeesFilters,
)
from dtos import (
    CreateEmployeeRequestDto,
    DeleteEmployeeRequestDto,
    EmployeeResponseDto,
    GetEmployeesResponseDto,
    CreateEmployeeResponseDto,
    DeleteEmployeeResponseDto,
)


ERROR_MAPPER: dict[str, HTTPException] = {
    "cannot find a object": HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="cannot find a object"
    )
}

router = APIRouter(prefix="/employees")


@router.get("/", response_model=GetEmployeesResponseDto, response_model_exclude_none=True)
@api_exception_handler(ERROR_MAPPER)
def get_employees_list(
    skip: int = Query(0),
    limit: int = Query(1000),
    employee_code: Optional[str] = Query(None),
    include_total: bool = False
) -> GetEmployeesResponseDto:
    request = QueryEmployeesRequest(
        filters=QueryEmployeesFilters(employee_code=employee_code),
        skip=skip,
        limit=limit,
        include_total=include_total
    )
    response = service.queryEmployees(request)
    employees = [
        EmployeeResponseDto(
            id=e.id,
            name=e.name,
            employee_code=e.employee_code,
            salary=e.salary,
        )
        for e in response.data
    ]
    return GetEmployeesResponseDto(data=employees, total=response.total)


@router.get("/{employee_code}", response_model=Optional[EmployeeResponseDto])
@api_exception_handler(ERROR_MAPPER)
def get_employee(employee_code: str) -> Optional[EmployeeResponseDto]:
    request = QueryEmployeesRequest(
        filters=QueryEmployeesFilters(employee_code=employee_code),
        limit=1,
    )
    response = service.queryEmployees(request)
    if not response.data:
        return None
    e = response.data[0]
    return EmployeeResponseDto(
        id=e.id,
        name=e.name,
        employee_code=e.employee_code,
        salary=e.salary,
    )


@router.post("/", response_model=CreateEmployeeResponseDto)
@api_exception_handler(ERROR_MAPPER)
def create_employee(body: CreateEmployeeRequestDto) -> CreateEmployeeResponseDto:
    employee = Employee(
        name=body.name,
        employee_code=body.employee_code,
        salary=body.salary,
    )
    request = ManageEmployeesRequest(create=employee)
    success = service.manageEmployees(request)
    return CreateEmployeeResponseDto(success=success)


@router.delete("/", response_model=DeleteEmployeeResponseDto)
@api_exception_handler(ERROR_MAPPER)
def delete_employee(body: DeleteEmployeeRequestDto) -> DeleteEmployeeResponseDto:
    delete = DeleteEmployee(id=body.id, employee_code=body.employee_code)
    request = ManageEmployeesRequest(delete=delete)
    success = service.manageEmployees(request)
    return DeleteEmployeeResponseDto(success=success)
