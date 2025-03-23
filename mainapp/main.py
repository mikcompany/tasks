from fastapi import FastAPI, HTTPException
from tasks.task_repositories import InMemoryTaskRepository
from tasks.task_repository import TaskRepository
from tasks.models import Task, TaskCreate, TaskUpdate
from tasks.models import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

repository: TaskRepository = InMemoryTaskRepository()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/tasks")
def list_tasks():
    return repository.list_tasks()

@app.post("/tasks")
def create_task(task_create: TaskCreate):
    task = repository.create_task(task_create)
    if not task:
        raise HTTPException(500, detail="Task creation failed")
    return task

@app.get("/tasks/{task_id}", response_model=Task, responses={404: {"description": "Task not found"}})
def read_task(task_id: int) -> Task:
    task = repository.get_task(task_id)
    if not task:
        raise HTTPException(404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task, responses={404: {"description": "Task not found"}})
def update_task(task_id: int, task_update: TaskUpdate) -> Task:
    task = repository.update_task(task_id, task_update)
    if not task:
        raise HTTPException(404, detail="Task not found")
    return Task(id=task_id, **task_update.dict())

@app.delete("/tasks/{task_id}", response_model=Task, responses={404: {"description": "Task not found"}})
def delete_task(task_id: int) -> Task:
    task = repository.delete_task(task_id)
    if not task:
        raise HTTPException(404, detail="Task not found")
    return task
