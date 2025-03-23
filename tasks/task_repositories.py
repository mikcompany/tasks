from .models import TaskCreate, Task, TaskUpdate
import itertools
from typing import Optional
from .task_repository import TaskRepository
from sqlmodel import SQLModel, create_engine, Session, delete, select


class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self._id_gen = itertools.count(start=1)

    def list_tasks(self) -> list[Task]:
        return list(self.tasks.values())

    def create_task(self, task_create: TaskCreate) -> Optional[Task]:
        task_id = next(self._id_gen)
        self.tasks[task_id] = Task(id=task_id, **task_create.model_dump())
        return self.tasks[task_id]

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.tasks.get(task_id)

    def update_task(self, task_id: int, task_update: TaskUpdate):
        task = self.tasks.get(task_id)
        if task:
            task.description = (
                task_update.description if task_update.description else task.description
            )
            task.done = task_update.done if task_update.done is not None else task.done
        return task

    def delete_task(self, task_id: int):
        return self.tasks.pop(task_id, None)

    def truncate(self):
        self.tasks.clear()


class SqliteTaskRepository(TaskRepository):
    def __init__(self, db_name: str):
        self.engine = create_engine(
            f"sqlite:///{db_name}", connect_args={"check_same_thread": False}
        )
        SQLModel.metadata.create_all(self.engine)

    def list_tasks(self) -> list[Task]:
        tasks: list[Task] = []
        with Session(self.engine) as session:
            tasks = list(session.exec(select(Task)).all())
        return tasks

    def create_task(self, task_create: TaskCreate) -> Optional[Task]:
        task = Task(**task_create.model_dump())
        with Session(self.engine) as session:
            session.add(task)
            session.commit()
            session.refresh(task)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        with Session(self.engine) as session:
            task = session.get(Task, task_id)
        return task

    def update_task(self, task_id: int, task_update: TaskUpdate):
        with Session(self.engine) as session:
            task = session.get(Task, task_id)
            if task:
                task.description = (
                    task_update.description
                    if task_update.description
                    else task.description
                )
                task.done = (
                    task_update.done if task_update.done is not None else task.done
                )
            session.commit()
            session.refresh(task)
        return task

    def delete_task(self, task_id: int):
        with Session(self.engine) as session:
            task = session.get(Task, task_id)
            if task:
                session.delete(task)
                session.commit()
        return task

    def truncate(self):
        with Session(self.engine) as session:
            session.execute(delete(Task))
            session.commit()
