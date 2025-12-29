from pydantic import Field
from manage_employees.types import Employee


class CreateEmployeeRequestDto(Employee):
    employee_code: str = Field(
        min_length=5,
        max_length=5,
        description="employee_code should be string with length=5"
    )
