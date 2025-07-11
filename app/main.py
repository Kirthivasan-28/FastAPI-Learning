from fastapi import FastAPI
from app.api.v1 import todo

app = FastAPI(title="Todo API", version="1.0")
app.include_router(todo.router, prefix="/api/v1/todo", tags=["Todos"])