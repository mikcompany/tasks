from typing import Protocol
from tasks.models import Task, TaskCreate, TaskUpdate
from typing import Optional


class TaskRepository(Protocol):
    def list_tasks(self) -> Optional[list[Task]]:
        pass

    def create_task(self, task_create: TaskCreate) -> Optional[Task]:
        pass

    def get_task(self, task_id: int) -> Optional[Task]:
        pass

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        pass

    def delete_task(self, task_id: int) -> Optional[Task]:
        pass
