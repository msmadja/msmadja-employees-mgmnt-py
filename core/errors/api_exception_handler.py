from functools import wraps
from typing import Callable

from fastapi import HTTPException, status


def api_exception_handler(error_mapper: dict[str, HTTPException] = {}):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except HTTPException:
                raise
            except Exception as e:
                raise error_mapper.get(str(e), HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="unexpected error happens"
                ))
        return wrapper
    return decorator
