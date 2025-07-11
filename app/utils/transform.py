# app/utils/transform.py

def normalize_todo(todo: dict) -> dict:
    todo["id"] = str(todo["_id"])
    del todo["_id"]
    return todo
