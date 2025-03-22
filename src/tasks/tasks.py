from pydantic import BaseModel

class TaskBase(BaseModel):
    description: str

class Task(TaskBase):
    id: int
    done: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    done: bool
    pass

class TaskDelete(Task):
    pass
