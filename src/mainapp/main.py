from fastapi import FastAPI, HTTPException
from tasks.task_repositories import InMemoryTaskRepository
from tasks.tasks import Task, TaskCreate, TaskUpdate, TaskDelete

app = FastAPI()

in_memory_task_repository = InMemoryTaskRepository()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/tasks")
def list_tasks() -> list[Task]:
    return list(in_memory_task_repository.tasks.values())

@app.post("/tasks")
def create_task(task_create: TaskCreate) -> Task:
    task = in_memory_task_repository.create_task(task_create)
    return task

@app.get("/tasks/{task_id}", response_model=Task, responses={404: {"description": "Task not found"}})
def read_task(task_id: int) -> Task:
    task = in_memory_task_repository.get_task(task_id)
    if not task:
        raise HTTPException(404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task, responses={404: {"description": "Task not found"}})
def update_task(task_id: int, task_update: TaskUpdate) -> Task:
    task = in_memory_task_repository.update_task(task_id, task_update)
    if not task:
        raise HTTPException(404, detail="Task not found")
    return Task(id=task_id, **task_update.dict())

@app.delete("/tasks/{task_id}", response_model=TaskDelete, responses={404: {"description": "Task not found"}})
def delete_task(task_id: int) -> Task:
    task = in_memory_task_repository.delete_task(task_id)
    if not task:
        raise HTTPException(404, detail="Task not found")
    return task
