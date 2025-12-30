from fastapi import FastAPI
from core import method_middlewares
from controllers import employees_controller

app = FastAPI()
app.include_router(employees_controller)

for middleware in method_middlewares:
    app.middleware("http")(middleware)


@app.get("/")
def root():
    return {"message": "Server is running!"}
