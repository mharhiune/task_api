from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from typing import List, Optional

app = FastAPI()

class Task(BaseModel):
    id: int
    task: str
    description: str = None
    completed: bool = False

class TaskUpdate(BaseModel):
    id: int 
    task: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# My database
tasks = [
    {"id": 1,
    "task": "Laudry",
    "description": "My clothes first, then mom and dad"
    },
    {"id": 2,
    "task": "Dishes",
    "description": "Cutlery only"
    },
    {"id": 3,
    "task": "Scrub",
    "description": "Children bathroom"
    },
    {"id": 4,
    "task": "Remove cobwebs",
    "description": "In the hall"
    }
]

# Task endpoints

@app.get("/")
def get_home():
    return {"message": "Hey there! Welcome to your task manager.😊"}

# GET: View all tasks
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks 

# POST: Create a new task
@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return {"message": "Yippeee!!! You have successfully added a new task."}

# PUT: Edit a task
@app.put("/tasks")
def update_task(task_id: int, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if task_update.task is not None:
                task["title"] = task_update.task
            if task_update.description is not None:
                task["description"] = task_update.description
            if task_update.completed is not None:
                task["completed"] = task_update.completed
            return {"message": "Hey there! You have successfully updated your task.😊"}
    raise HTTPException(status_code=404, detail="Task not found")

# DELETE: Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(index)
            return {"message": "Task deleted succesfully", "task": deleted_task}
    raise HTTPException(status_code=404, detail="Task not found")