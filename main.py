from fastapi import FastAPI
from controllers import employees_controller

app = FastAPI()
app.include_router(employees_controller)

@app.get("/")
def root():
    return { "message": "Server is running!" }