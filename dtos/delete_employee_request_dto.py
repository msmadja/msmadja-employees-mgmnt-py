from typing import Optional
from pydantic import Field
from manage_employees.types import DeleteEmployee


class DeleteEmployeeRequestDto(DeleteEmployee):
    employee_code: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=5,
        description="employee_code should be string with length=5"
    )
