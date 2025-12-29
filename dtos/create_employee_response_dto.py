from pydantic import BaseModel


class CreateEmployeeResponseDto(BaseModel):
    success: bool
