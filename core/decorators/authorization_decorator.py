from functools import wraps
from fastapi import Request, HTTPException, status

def authorize(arg_name: str = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            if not request:
                raise ValueError("Request object not found for bearer token check")
            
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Missing or invalid Authorization header",
                )
            
            token = auth_header[len("Bearer "):].strip()

            # validate the token by the idp

            return await func(*args, **kwargs)
        return wrapper
    return decorator