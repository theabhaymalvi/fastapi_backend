from fastapi import APIRouter, HTTPException
from models import Task
from db_connection import tasks_collection
from bson import ObjectId

router = APIRouter()

@router.get("/")
def getTasks(userId: str):
    try:
        tasks = tasks_collection.find({"userId": userId})
        tasks_list = []
        for task in tasks:
            task["_id"] = str(task["_id"])
            tasks_list.append(task)
        return {"data": tasks_list}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/")
def addTask(task: Task):
    try:
        task = task.model_dump()
        result = tasks_collection.insert_one(task)
        print(result)
        return {"success": True, "msg": "Task created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/")
def deleteTask(taskId: str):
    try:
        task = tasks_collection.find_one({"_id": ObjectId(taskId)})

        if not task:
            raise HTTPException(status_code=400, detail="Task not found")
        
        result = tasks_collection.delete_one({"_id": ObjectId(taskId)})
        print(result)
        return {"success": True, "msg": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/")
def updateTask(taskId: str, update_data: dict):
    if "_id" in update_data:
        del update_data["_id"]
    try:
        updated_task = tasks_collection.find_one_and_update({"_id": ObjectId(taskId)}, {"$set": update_data})

        if updated_task:
            return {"success": True, "msg": "Task updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Task not found") 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
