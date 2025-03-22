from .tasks import Task, TaskCreate, TaskUpdate
import itertools

class InMemoryTaskRepository:
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self._id_gen = itertools.count(start=1)

    def create_task(self, task_create: TaskCreate) -> Task:
        task_id = next(self._id_gen)
        self.tasks[task_id] = Task(id=task_id, **task_create.model_dump())
        return self.tasks[task_id]

    def get_task(self, task_id: int) -> Task | None:
        return self.tasks.get(task_id)

    def update_task(self, task_id: int, task_update: TaskUpdate):
        task = self.tasks.get(task_id)
        if task:
            task.description = task_update.description
            task.done = task_update.done
        return task

    def delete_task(self, task_id: int):
        return self.tasks.pop(task_id, None)
