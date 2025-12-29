from pydantic import BaseModel


class DeleteEmployeeResponseDto(BaseModel):
    success: bool
