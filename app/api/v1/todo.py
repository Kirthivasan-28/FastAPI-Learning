from fastapi import APIRouter, status, HTTPException, Body
from app.models.todo import TodoCreate, TodoResponse
from typing import List
from app.db.mongo import db
from bson import ObjectId
from datetime import datetime, timezone
from app.utils.transform import normalize_todo
router = APIRouter()

@router.post("/",response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    todo_dict = todo.model_dump()
    todo_dict["created_at"] = datetime.now(timezone.utc)
    result = await db.todos.insert_one(todo_dict)
    todo_dict["id"]=str(result.inserted_id)
    return normalize_todo(todo_dict)

@router.get("/",response_model=List[TodoResponse])
async def get_all_todos():
    todos = []
    async for todo in db.todos.find():
        todo["id"]=str(todo["_id"])
        todos.append(normalize_todo(todo))
    return todos

@router.get("/{todo_id}",response_model=TodoResponse)
async def get_todo_by_id(todo_id: str):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="invalid ID Format")
    
    todo = await db.todos.find_one({"_id":ObjectId(todo_id)})
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    
    todo["id"]= str(todo["_id"])
    return normalize_todo(todo)

@router.put("/{todo_id}",response_model=TodoResponse)
async def update_todo_by_id(todo_id:str, updated_todo: TodoCreate=Body(...)):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="invalid ID Format")
    
    result = await db.todos.find_one_and_update(
        {"_id":ObjectId(todo_id)},
        {"$set":updated_todo.model_dump(),"updated_at":datetime.now(timezone.utc)},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    
    result["id"]= str(result["_id"])
    return normalize_todo(result)


@router.delete("/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id:str):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="invalid ID Format")
    
    result = await db.todos.delete_one(
        {"_id":ObjectId(todo_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    
    return 
        